#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-22

"""Stuff that differs in different Python versions"""

import sys


console_encoding = sys.__stdout__.encoding

if sys.version_info >= (3,):
    from urllib.error import URLError, HTTPError
    from queue import Queue, Empty
    from urllib.request import url2pathname, urlretrieve
    from email import message as emailmessage
    import socketserver as SocketServer
    import urllib.parse as urllib
    import urllib.request as urllib2
    import urllib.parse as urlparse
    import xmlrpc.client as xmlrpclib
    import http.client as httplib

    import tkinter as tk
    from tkinter import ttk
    from tkinter.font import Font
    from tkinter.filedialog import (askdirectory, askopenfilename,
         asksaveasfilename)
    from tkinter.messagebox import (showinfo, showwarning, showerror,
         askquestion, askokcancel, askyesno, askretrycancel)

    class aStr():
        def __str__(self):
            return self.__unicode__()

    def cmp(a, b):
        return (a > b) - (a < b)

    def b(s):
        return s.encode('utf-8')

    def u(s):
        return s.decode('utf-8')

    def console_to_str(s):
        try:
            return s.decode(console_encoding)
        except UnicodeDecodeError:
            return s.decode('utf_8')

    def fwrite(f, s):
        f.buffer.write(b(s))

#   bytes = bytes
    unicode = str

    string_types = str,
    numeric_types = int, float, complex
    simple_types = int, float, complex, str, bytearray
    collections_types = list, tuple, set, frozenset
    all_types = (int, float, complex, str, bytearray,
                 list, tuple, set, frozenset, dict)

else:
    from urllib2 import URLError, HTTPError
    from Queue import Queue, Empty
    from urllib import url2pathname, urlretrieve
    from email import Message as emailmessage
    import SocketServer
    import urllib
    import urllib2
    import urlparse
    import xmlrpclib
    import httplib

    import Tkinter as tk
    import ttk
    from tkFont import Font
    from tkFileDialog import (askdirectory, askopenfilename,
         asksaveasfilename)
    from tkMessageBox import (showinfo, showwarning, showerror,
         askquestion, askokcancel, askyesno, askretrycancel)

    class aStr():
        def __str__(self):
            return self.__unicode__().encode('utf-8')

#   cmp = cmp
    range = xrange

    def b(s):
        return s

    def u(s):
        return s

    def console_to_str(s):
        return s

    def fwrite(f, s):
        f.write(s)

    bytes = str
#   unicode = unicode

    string_types = basestring,
    numeric_types = int, long, float, complex
    simple_types = int, long, float, complex, basestring, bytearray
    collections_types = list, tuple, set, frozenset
    all_types = (int, long, float, complex, basestring, bytearray,
                 list, tuple, set, frozenset, dict)
