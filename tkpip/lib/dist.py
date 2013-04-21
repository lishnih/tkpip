#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

import logging
from pip.commands import install


def dist_install(dist):
    installcommand = install.InstallCommand()
    options, args = installcommand.parser.parse_args([dist])
    try:
        installcommand.run(options, args)
    except Exception as e:   # DistributionNotFound
        logging.error(e)


def dist_upgrade(dist):
    installcommand = install.InstallCommand()
    options, args = installcommand.parser.parse_args(['-U', dist])
    try:
        installcommand.run(options, args)
    except Exception as e:   # DistributionNotFound
        logging.error(e)
