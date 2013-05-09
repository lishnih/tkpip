#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, logging

from .backwardcompat import *


# recipe from http://code.activestate.com/recipes/410646-tkinter-listbox-example/
class ListBoxData(tk.Listbox):
    def __init__(self, master=None):
        self.v = tk.Variable(master)
        tk.Listbox.__init__(self, master, listvariable=self.v)
        ListBoxData.clear(self)

    def clear(self):
        self.v.set(())
        self._selected = None
        self._datas = []

    def __iter__(self):
        values = self.v.get()
        for i in range(len(values)):
            yield i, self.value(i), self.data(i)

    def value(self, pos):
        try:
            pos = self.index(pos)
            values = self.v.get()
            return values[pos]
        except ValueError as e: # !!! ValueError: invalid literal for int() with base 10: 'None'
            print(pos, e)

    def data(self, pos):
        try:
            pos = self.index(pos)
            return self._datas[pos]
        except ValueError as e: # !!! ValueError: invalid literal for int() with base 10: 'None'
            print(pos, e)

    def setValue(self, pos, value):
        pos = self.index(pos)
        values = list(self.v.get())
        values[pos] = value
        self.v.set(tuple(values))

    def setData(self, pos, data):
        pos = self.index(pos)
        self._datas[pos] = data

    def get_selected(self):
        if self._selected is None:
            return None, None, None
        try:
            value = self.value(self._selected)
            data = self.data(self._selected)
        except IndexError:
            logging.warning("Index Error: {0}!".format(self._selected))
            value = None
            data = None
        return self._selected, value, data

#     def delete(self, pos1, pos2=None):
#         pos1 = self.index(pos1)
#         pos2 = self.index(pos2)
#         Listbox.delete(self, pos1, pos2)
#         del self.v[pos1:pos2+1]
#         del self._datas[pos1:pos2+1]

    def insert(self, pos, label, **kw):
        self.insert_data(pos, label, None, **kw)

    def insert_data(self, pos, label, data, **kw):
        pos = self.index(pos)
        tk.Listbox.insert(self, pos, label, **kw)
        self._datas.insert(pos+1, data)

        # itemconfig
        if data:
            itemconfig = data.get('_item')
            if itemconfig:
                self.itemconfig(pos, **itemconfig)

    def insert_items(self, items):
        if isinstance(items, list):
            for key in sorted(items):
                self.insert(tk.END, key)
        elif isinstance(items, dict):
            for key in sorted(items.keys()):
                self.insert_data(tk.END, key, items[key])


def test():
    root = Tk()

    # Listbox Widget
    listbox1 = ListBoxData(root)
    lb1_yscrollbar = Scrollbar(root, orient=tk.VERTICAL, command=listbox1.yview)
    listbox1['yscrollcommand'] = lb1_yscrollbar.set

    # Pack
    listbox1.pack(side = 'left', fill = 'both', expand = 1)
    lb1_yscrollbar.pack(side = 'right', fill = 'both')

    # Main loop
    root.mainloop()


if __name__ == '__main__':
    test()
