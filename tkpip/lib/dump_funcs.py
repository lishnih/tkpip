#!/usr/bin/env python
# coding=utf-8
# Stan 2007-08-02

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys

from .backwardcompat import *


def plain(obj, level=0):
    wrap = " " * 4 * level

    if obj is None:
        buf = "/is None/"
        return buf

    if isinstance(obj, (int, float, complex, string_types, bytearray)):
        buf = "'{0}'".format(unicode(obj))
        return buf

    if isinstance(obj, list):
        buf = "[\n"
        for key in obj:
            buf += wrap + "    {0}\n".format(plain(key, level+1))
        buf += wrap + "]"
        return buf

    if isinstance(obj, tuple):
        buf = "(\n"
        for key in obj:
            buf += wrap + "    {0}\n".format(plain(key, level+1))
        buf += wrap + ")"
        return buf

    if isinstance(obj, dict):
        buf = "{\n"
        for key, val in obj.items():
            buf += wrap + "    {0:16}: {1}\n".format(key, plain(val, level+1))
        buf += wrap + "}"
        return buf

    buf = "{0}{{\n".format(type(obj))
    for key in dir(obj):
        val = getattr(obj, key)
        if key[0:2] != '__' and not callable(val):
            buf += wrap + "    {0:16}: {1}\n".format(key, plain(val, level+1))
    buf += wrap + "}"
    return buf
