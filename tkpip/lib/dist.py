#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging
from pip.commands import install
from pip.baseparser import ConfigOptionParser


def dist_install(dist):
    parser = ConfigOptionParser(name=dist)
    installcommand = install.InstallCommand(parser)
    options, args = installcommand.parser.parse_args([dist])
    try:
        installcommand.run(options, args)
    except Exception as e:   # DistributionNotFound
        logging.error(e)
    print("finished!")        


def dist_upgrade(dist):
    parser = ConfigOptionParser(name=dist)    
    installcommand = install.InstallCommand(parser)
    options, args = installcommand.parser.parse_args(['-U', dist])
    try:
        installcommand.run(options, args)
    except Exception as e:   # DistributionNotFound
        logging.error(e)
    print("finished!")
