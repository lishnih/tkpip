#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

import sys

if sys.version_info >= (3, 0):
    from tkinter import *
else:
    from Tkinter import *

from dump_funcs import plain
from listboxdata import ListBoxData
from dist import *


class ListBoxText(ListBoxData):
    def __init__(self, master=None, text=None, cache={}):
        ListBoxData.__init__(self, master)
        self._text = text
        self._cache = cache

    def clear(self):
        ListBoxData.clear(self)
        self._text.delete(1.0, END)

    def onClicked(self, event=None):
        selection = self.curselection()
        if selection:
            self._selected = int(selection[0])

            if self._text:
                self._text.delete(1.0, END)
                selected, value, data = self.get_selected()

                if data is None:
                    text = u"No data!"
                    self._text.insert(END, text)
                    return

                key = data.get('key')
                if key is None:
                    text = u"Wrong data!"
                    self._text.insert(END, text)
                    return

                # Информация об установленном пакете
                dist = data.get('dist')
                if dist:
                    installed = dist.version
                    state = u"active" if data['active'] else u"non-active"
                    dist_dump = plain(dist)
                else:
                    installed = u"<Not installed>"
                    state = 'none'
                    dist_dump = u"none\n"

                # Информация из Pypi
                name, ver, data, urls, releases = self._cache.get(key)
                data_dump = plain(data)
                urls_dump = u''
                for i in urls:
                    urls_dump += "{}\n---\n".format(plain(i))

                text = u"""{} [{}] ({})
Installed: {}
Latest:    {} {!r}

=== Dist dump
{}
=== Data dump
{}
=== Urls dump
{}""".format(key, name, state, installed, ver, releases, dist_dump, data_dump, urls_dump)

                self._text.insert(END, text)

    def onActivated(self, event=None):
        selected, value, data = self.get_selected()
        if data is None:
            dist = value
            print("Installing {}".format(dist))
            dist_install(dist)
        else:
            dist = data['dist'].key
            print("Upgrading {}".format(dist))
            dist_upgrade(dist)
