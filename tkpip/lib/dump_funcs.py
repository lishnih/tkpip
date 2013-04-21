# coding=utf-8
# Stan 2007-08-02

import sys

""" Отладочный вывод переменных различных типов
    сокращённая версия
"""


def plain_val(obj):
    if obj is None:
        buf = u'/is None/'
    elif isinstance(obj, (int, float, long, complex)):
        buf = unicode(obj)
    else:
        try:
            buf = unicode(obj)
        except:
            buf = repr(obj)
            buf = buf.replace(r'\n', '\n')
            buf = buf.replace(r'\r', '')

    return buf


def plain(obj):
    if sys.version_info >= (3, 0):
        return repr(obj)

    if obj is None or isinstance(obj, (int, float, long, complex, basestring, bytearray)):
        buf = plain_val(obj)
        return buf

    if isinstance(obj, (list, tuple)):
        buf = u''
        for key in obj:
            buf += u'  {}\n'.format(plain_val(key))
        return buf

    if isinstance(obj, dict):
        buf = u''
        for key, val in obj.items():
            buf += u'   {:18}: {}\n'.format(key, plain_val(val))
        return buf

    dirs_buf = u''
    for key in dir(obj):
        val = getattr(obj, key)
        if not callable(val):
            if key[0:2] != '__':
                dirs_buf += u'{:20}: {}\n'.format(key, plain_val(val))

    dirs_buf += u'\n'

    return dirs_buf
