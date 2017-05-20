# OwnCloud Backup
Script to making backup to your owncloud server.

## Requiremets
- Unix[-like] system
- Python 3
- [pyocclient](https://github.com/owncloud/pyocclient)
You can install pyocclient by running:
```bash
$ pip install pyocclient
```

## Installation
1. Create `config.json` file. (See `config.json.sample`)
2. Configure script by editing `config.json` file.

## Usage
Just run:
```bash
$ python 3 /path/to/install/dir/backup.py
```
you can run it from any directory.

## License
MIT
