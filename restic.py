#!/usr/bin/env python
import logging
import time
import argparse
import importlib.util
import os
import json
import subprocess
import pathlib


def backup(config):
    logging.info("start backup")
    for dir in config.directories:
        path = pathlib.Path(dir).expanduser()
        if not path.exists():
            logging.error(
                "{} is not a valid directory and will not be backed up. Continuing with rest of directories.".format(
                    path
                )
            )
            continue

        start = time.time()
        logging.info("backing up {}".format(path))
        args = ["restic", "-r", config.repository, "backup", "--json", path]
        if hasattr(config, "backup_args"):
            args += config.backup_args
        p = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
        )

        if p.returncode != 0:
            logging.error("backup up failed for {}:\n  {}".format(path, p.stderr))
            continue

        stdout = p.stdout.split("\n")
        for line in stdout:
            if not line:
                continue
            line = json.loads(line)
            if "message_type" in line and line["message_type"] == "summary":
                summary = line
                end = time.time()
                logging.info("successfully backed up {} in: {:.2} seconds".format(path, end - start))

    logging.info("backup finished")


def prune(config):
    start = time.time()
    logging.info("start prune")
    args = ["restic", "-r", config.repository, "forget", "--prune", "--json"]
    if hasattr(config, "prune_args"):
        args += config.prune_args
    p = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )

    if p.returncode != 0:
        logging.error("pruning failed:\n  {}".format(p.stderr))
        return

    end = time.time()
    logging.info("prune finished in {:.2} seconds".format(end - start))


def check(config):
    start = time.time()
    logging.info("start check")
    args = ["restic", "-r", config.repository, "check", "--json"]
    if hasattr(config, "check_args"):
        args += config.check_args
    p = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )

    if p.returncode != 0:
        logging.error("checking failed:\n  {}".format(p.stderr))
        return

    end = time.time()
    logging.info("check finished in {:.2} seconds".format(end - start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_file",
        help="Absolute path to configuration file.",
        type=str,
        default="~/.config/restic/restic_conf.py",
    )
    parser.add_argument(
        "--log_file",
        help="Absolute path to location of log file.",
        type=str,
        default="~/.local/share/restic/restic.log",
    )
    args = parser.parse_args()

    # Load config
    config_path = pathlib.Path(args.config_file).expanduser()
    if not config_path.exists():
        print("No config file found at: {}".format(args.config_file))
        exit(1)

    try:
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
    except FileNotFoundError as e:
        print(str(e))
        exit(1)

    # Setup logging
    log_path = pathlib.Path(args.log_file).expanduser()
    log_path.parents[0].mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_path,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )

    # Check if password/password_file/password_command is set
    if (
        "RESTIC_PASSWORD" not in os.environ
        and "RESTIC_PASSWORD_FILE" not in os.environ
        and "RESTIC_PASSWORD_COMMAND" not in os.environ
    ):
        logging.error(
            "No password found in environment variables. See restic documentation for more info"
        )
        exit(1)

    # Main
    backup(config)
    prune(config)
    check(config)
