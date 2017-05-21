# OwnCloud Backup
[![Build Status](https://travis-ci.org/nathiss/backup-owncloud.svg?branch=master)](https://travis-ci.org/nathiss/backup-owncloud)  
Script to making backup to your owncloud server.

## Requiremets
- Unix[-like] system
- Python >= 3.3
- [pyocclient](https://github.com/owncloud/pyocclient)

## Installation
1. Create `config.json` file. (See `config.json.sample`)
2. Configure script by editing `config.json` file.
3. Run `pip3 install -r requirements.txt`.

## Usage
Just run:
```bash
$ python3 /path/to/install/dir/backup.py
```
you can run it from any directory.

## License
MIT
