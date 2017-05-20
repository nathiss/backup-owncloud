#!/usr/bin/env python3
import os
import re
import sys
import json
import tempfile
import shutil
import tarfile
import datetime
import owncloud

# set env
install_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(install_dir)


def check_config(config):
    if "protocol" not in config:
        raise KeyError("Protocol parameter is required.")
    if "host" not in config:
        raise KeyError("Host parameter is required.")
    if "port" not in config:
        raise KeyError("Port parameter is required.")
    if "lognot in" in config:
        raise KeyError("Lognot in parameter is required.")
    if "passwd" not in config:
        raise KeyError("Passwd parameter is required.")
    if "verifyCerts" not in config:
        raise KeyError("VerifyConfig parameter is required.")
    if "remoteDir" not in config:
        raise KeyError("RemoteDir parameter is required.")
    if "useHashes" not in config:
        raise KeyError("UseHashes parameter is required.")
    if "files" not in config:
        raise KeyError("Files parameter is required.")

    if not re.compile('^http[s]?$').match(config['protocol']):
        raise ValueError("Protocol can be \"http\" or \"https\" only.")

    port = int(config['port'])
    if port < 1 or port > 65535:
        raise ValueError("Port is not valid.")

    if not (config['useHashes'] == "true" or config['useHashes'] == "false"):
        raise ValueError("UseHashes has to be \"true\" or \"false\".")

    if not (config['verifyCerts'] == "true" or
            config['verifyCerts'] == "false"):
        raise ValueError("VerifyCerts has to be \"true\" or \"false\".")

    if not isinstance(config['files'], list):
        raise ValueError("Files has to be an array.")

    pattern = re.compile("^/.+$")
    if any(not pattern.match(path) for path in config['files']):
        raise ValueError("Paths must be absolute.")


def getAllSubpaths(paths):
    result = []
    for path in paths:
        if os.path.isfile(path):
            result.append(path)
        else:
            for dir_path, _, filenames in os.walk(path):
                for f in filenames:
                    result.append(os.path.abspath(os.path.join(dir_path, f)))
    return result


def splitPaths(paths):
    result = []
    for path in paths:
        result.append(path.split('/')[1:])
    return result


def makeArchive(tmp_dir):
    name = datetime.datetime.now().strftime("%H.%M-%d-%m-%Y") + ".tar.xz"
    archive_path = os.path.join(tmp_dir, name)
    tar = tarfile.open(archive_path, "w:xz")
    for path in os.listdir(tmp_dir):
        tar.add(path)
    tar.close()
    return archive_path


def createTmpTree(files_paths):
    splited_paths = splitPaths(files_paths)
    tmp_dir_path = tempfile.mkdtemp(prefix='backup-')
    for idx, path in enumerate(splited_paths):
        os.chdir(tmp_dir_path)
        for parent_dir in path[:-1]:
            if not os.path.isdir(parent_dir):
                os.mkdir(parent_dir)
            os.chdir(parent_dir)
        shutil.copy2(files_paths[idx],
                     os.path.join(tmp_dir_path, files_paths[idx][1:]))
    os.chdir(tmp_dir_path)
    return tmp_dir_path


def getVerifyCerts(config):
    if config['verifyCerts'] == "true":
        return True
    return False


def main():
    print("[INFO]\tReading config.json file.")
    config = ""
    with open('config.json', 'r') as json_data:
        config = json.load(json_data)
    check_config(config)

    # TODO: checksums

    print("[INFO]\tGetting all subpaths.")
    files_paths = getAllSubpaths(config['files'])

    print("[INFO]\tCreating temporary directory tree.")
    tmp_dir_path = createTmpTree(files_paths)

    print("[INFO]\tCreating achive.")
    archive_path = makeArchive(tmp_dir_path)

    print("[INFO]\tSending to server.")
    oc = owncloud.Client(
           "%s://%s:%s" % (config["protocol"], config["host"], config["port"]),
           verify_certs=getVerifyCerts(config)
        )
    oc.login(config["login"], config["passwd"])
    oc.put_file(os.path.join(config["remoteDir"], archive_path.split("/")[-1]),
                archive_path)
    oc.logout()

    print("[INFO]\tDone.")

if __name__ == "__main__":
    main()

