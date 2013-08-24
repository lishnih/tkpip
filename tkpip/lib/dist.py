#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging
from pkg_resources import load_entry_point

install_func = load_entry_point('pip', 'console_scripts', 'pip')


def dist_install(name):
    print("Installing {0}".format(name))
    try:
        args = [
            'install',
            name,
        ]
        return install_func(args)
    except Exception as e:
        logging.exception(e)
    print("finished!")


def dist_upgrade(name):
    print("Upgrading {0}".format(name))
    try:
        args = [
            'install',
            '--upgrade',
            name,
        ]
        return install_func(args)
    except Exception as e:
        logging.exception(e)
    print("finished!")


def dist_uninstall(name, dist=None):
    if dist:
        name += "==" + dist.version

    print("Uninstalling {0}".format(name))
    try:
        args = [
            'uninstall',
            '-y',
            name,
        ]
        return install_func(args)
    except Exception as e:
        logging.exception(e)
    print("finished!")
