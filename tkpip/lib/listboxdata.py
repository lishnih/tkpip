#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

import sys, logging

if sys.version_info >= (3, 0):
    from tkinter import *
else:
    from Tkinter import *


# recipe from http://code.activestate.com/recipes/410646-tkinter-listbox-example/
class ListBoxData(Listbox):
    def __init__(self, master=None):
        Listbox.__init__(self, master)
        ListBoxData.clear(self)

    def clear(self):
        Listbox.delete(self, 0, END)
        self._selected = None
        self._values = []
        self._datas = []

    def __iter__(self):
        for i in range(len(self._values)):
            yield i, self._values[i], self._datas[i]

    def value(self, pos):
        pos = self.index(pos)
        return self._values[pos]

    def data(self, pos):
        pos = self.index(pos)
        return self._datas[pos]

    def setValue(self, pos, value):
        pos = self.index(pos)
        self._values[pos] = value

    def setData(self, pos, data):
        pos = self.index(pos)
        self._datas[pos] = data

    def get_selected(self):
        try:
            value = self._values[self._selected]
            data = self._datas[self._selected]
        except IndexError:
            logging.warning("Index Error: {}!".format(self._selected))
            value = None
            data = None
        return self._selected, value, data

    def delete(self, pos1, pos2=None):
        pos1 = self.index(pos1)
        pos2 = self.index(pos2)
        Listbox.delete(self, pos1, pos2)
        del self._values[pos1:pos2+1]
        del self._datas[pos1:pos2+1]

    def insert(self, pos, label, **kw):
        self.insert_data(pos, label, None, **kw)

    def insert_data(self, pos, label, data, **kw):
        pos = self.index(pos)
        Listbox.insert(self, pos, label, **kw)
        self._values.insert(pos+1, label)
        self._datas.insert(pos+1, data)

        # itemconfig
        if data:
            itemconfig = data.get('_item')
            if itemconfig:
                self.itemconfig(pos, **itemconfig)

    def insert_items(self, items):
        if isinstance(items, list):
            for key in sorted(items):
                self.insert(END, key)
        elif isinstance(items, dict):
            for key in sorted(items.keys()):
                self.insert_data(END, key, items.get(key))


def test():
    root = Tk()

    # Listbox Widget
    listbox1 = ListBoxData(root)
    lb1_yscrollbar = Scrollbar(root, orient=VERTICAL, command=listbox1.yview)
    listbox1['yscrollcommand'] = lb1_yscrollbar.set

    # Pack
    listbox1.pack(side = 'left', fill = 'both', expand = 1)
    lb1_yscrollbar.pack(side = 'right', fill = 'both')

    # Main loop
    root.mainloop()


if __name__ == '__main__':
    test()
