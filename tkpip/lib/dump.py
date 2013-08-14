#!/usr/bin/env python
# coding=utf-8
# Stan 2007-08-02

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

try:    from .backwardcompat import *
except: from backwardcompat import *


""" Отладочный вывод переменных
plain_type возвращает тип объекта
plain      вывод переменной
"""


def plain_type(obj):
    buf = unicode(type(obj)).replace("'", "").replace("type ", "")\
          .replace("class ", "").replace("<", "[").replace(">", "]")
    return buf


def plain(obj, level=0):
    if obj is None:
        buf = "None"
        return buf

    if isinstance(obj, numeric_types):
        buf = unicode(obj)
        return buf

    if isinstance(obj, bytes):
        try:    buf = "'{0}'".format(u(obj).rstrip('\r\n'))
        except: buf = "repr: {0!r}".format(obj)
        return buf

    if isinstance(obj, string_types):
        try:    buf = "'{0}'".format(unicode(obj).rstrip('\r\n'))
        except: buf = "repr: {0!r}".format(obj)
        return buf

    if isinstance(obj, simple_types):
        buf = "'{0}'".format(unicode(obj))
        return buf

    if level > 5:
        return repr(obj)

    buf = ""
    wrap = " " * 4 * level

    if isinstance(obj, list):
        if obj:
            buf += "[\n"
            for key in obj:
                buf += wrap + "    {0}\n".format(plain(key, level+1))
            buf += wrap + "]"
        else:
            buf += "[]"
        return buf

    if isinstance(obj, collections_types):
        buf += "("
        for key in obj:
            buf += "{0}, ".format(plain(key, level+1))
        buf += ")"
        return buf

    if isinstance(obj, dict):
        buf += "{\n"
        for key in sorted(obj.keys()):
            val = obj[key]
            buf += wrap + "    {0:16}: {1}\n".format(key, plain(val, level+1))
        buf += wrap + "}"
        return buf

    if level > 2:
        return repr(obj)

    buf += "{0}{{\n".format(plain_type(obj))
    for key in dir(obj):
        try:                   val = getattr(obj, key)
        except Exception as e: val = "*** {0} ***".format(e)
        if key[0:2] != '__' and not callable(val):
            buf += wrap + "    {0:16}: {1}\n".format(key, plain(val, level+1))
    buf += wrap + "}}"
    return buf
