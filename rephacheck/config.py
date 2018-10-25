#!/usr/bin/env python3

"""
Determine by voting which is the state of each node.
For this to work properly, you need to have an odd number of nodes.
"""

import json
from os import environ
from pathlib import Path

import toml


def config(cli_args: dict = None) -> dict:
    """Get configuration options.

    Configuration options are loaded with this priority order:
    - CLI arguments
    - configuration file defined through CLI
    - environment variables
    - local configuration file
    - distribution configuration file
    - defaults

    :param cli_args: Configuration options coming from CLI call
    :type cli_args: dict
    :return: A dictionnary of configuration options
    :rtype: dict
    """

    # default conf
    conf = {
        "listen": "127.0.0.1",
        "port": 8543,
        "local_node_id": None,
        "nodes": {},
        "conninfo": {},
    }

    # paths
    if cli_args and "config_file" in cli_args:
        cli_conf = Path(str(cli_args.get("config_file")))
    dist_conf = Path("/etc/rephacheck/config.toml")
    local_conf = Path("/etc/rephacheck/config.local.toml")
    json_conf = Path("/etc/rephacheck.json")

    # use toml conf if exists and env conf not defined
    if dist_conf.exists() and "cli_conf" not in locals():
        with dist_conf.open() as conf_handler:
            conf.update(toml.load(conf_handler))
        # override with local config file exists
        if local_conf.exists():
            with local_conf.open() as local_handler:
                conf.update(toml.load(local_handler))
    # for backward compatibility, use json conf if exists
    elif json_conf.exists() and "cli_conf" not in locals():
        with json_conf.open() as conf_handler:
            conf.update(json.load(conf_handler))
        # timeout have been moved in conninfo section under connect_timeout name
        if "timeout" in conf:
            conf["conninfo"] = {"connect_timeout": conf.pop("timeout")}

    # override with environment variables if defined
    for item in conf:
        envvar = "REPHA_{}".format(item).upper()
        if envvar in environ:
            # nodes and conninfo must be dict objects
            if item in ("nodes", "conninfo"):
                conf[item] = json.loads(str(environ.get(envvar)))
            else:
                conf[item] = environ.get(envvar)

    # use cli conf if defined and exists
    if "cli_conf" in locals() and cli_conf.exists():
        with cli_conf.open() as env_handler:
            conf.update(toml.load(env_handler))

    # override with CLI arguments
    if cli_args:
        conf.update(cli_args)

    return conf
