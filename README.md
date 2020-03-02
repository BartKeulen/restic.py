# Python Restic Wrapper
`restic.py` is a simple wrapper for [restic](https://restic.net/), executing the following three tasks: backup, prune and check. A simple config file specifies the restic repository, directories to backup and arguments for each restic command. (See `examples/restic_conf.py` for an example config file).

## Installation
`restic.py` only requires restic to be installed on your system, see [restic documentation](https://restic.net/#installation) for more information. (And `Python 3`, but that should be standard by now).


## Usage
Initialize a `restic repository`, fill in your `restic_conf.py` configuration file and you are good to go. 

By default `restic.py` looks at `~/.config/restic/restic.conf` for the configuration file, but you can also pass in the absolute path as command line argument using the option `--config_file` (run `restic.py --help` for more information).

All logs are standard written to `~/.local/share/restic/restic.log` unless a different log file is specified via the `--log_file` command line option (run `restic.py --help` for more information).