#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, pkg_resources

from .backwardcompat import *
from .cache import pipcache
from .dist import *
from .dump_funcs import plain
from .listboxdata import ListBoxData


class ListBoxText(ListBoxData):
    def __init__(self, master=None, text=None):
        ListBoxData.__init__(self, master)
        self._text = text

    def clear(self):
        ListBoxData.clear(self)
        self._text.delete(1.0, tkinter.END)

    def onClicked(self, event=None):
        selection = self.curselection()
        if selection:
            self._selected = int(selection[0])

            if self._text:
                self._text.delete(1.0, tkinter.END)
                selected, value, data = self.get_selected()

                if data is None:
                    text = "No data!"
                    self._text.insert(tkinter.END, text)
                    return

                key = data.get('key')
                if key is None:
                    text = "Wrong data!"
                    self._text.insert(tkinter.END, text)
                    return

                # Информация об установленном пакете
                dist = data.get('dist')
                if dist:
                    installed = dist.version
                    state = "active" if data['active'] else "non-active"
                    dist_dump = plain(dist)
                else:
                    installed = "<Not installed>"
                    state = 'none'
                    dist_dump = "none\n"

                # Информация из Pypi
                name, ver, data, urls, releases = pipcache.get(key)
                data_dump = plain(data)
                urls_dump = ""
                for i in urls:
                    urls_dump += "{0}\n---\n".format(plain(i))

                text = """{0} [{1}] ({2})
Installed: {3}
Latest:    {4} {5!r}

=== Dist dump
{6}
=== Data dump
{7}
=== Urls dump
{8}""".format(key, name, state, installed, ver, releases, dist_dump, data_dump, urls_dump)

                self._text.insert(tkinter.END, text)

    def onActivated(self, event=None):
        selected, value, data = self.get_selected()
        key = data.get('key')
        if key:
            if '[I]' in value:
                self.pkgInstall(key, selected)
            elif '[U]' in value:
                self.pkgUpgrade(key, selected)

    def onInstall(self, event=None):
        selected, value, data = self.get_selected()
        key = data.get('key')
        if key:
            self.pkgInstall(key, selected)

    def onUpgrade(self, event=None):
        selected, value, data = self.get_selected()
        key = data.get('key')
        if key:
            self.pkgUpgrade(key, selected)

    def pkgInstall(self, key, selected):
        print("Installing {0}".format(key))
        dist_install(key)
        self.update_value(key, selected)

    def pkgUpgrade(self, key, selected):
        print("Upgrading {0}".format(key))
        dist_upgrade(key)
        self.update_value(key, selected)

    def update_value(self, key, selected):
        distros = pkg_resources.Environment()
        dist = distros[key]
        dist = dist[0] if dist else None

        if dist:
            installed = dist.version

            data = self.data(selected)
            data['active'] = True   # !!!
            data['dist'] = dist
            data['_item'] = {}
            label = "{0} {1}".format(key, installed)
            self.setValue(selected, label)

            name, ver, data, urls, releases = pipcache.get(key)
            if installed == ver:
                self.itemconfig(selected, background='')
