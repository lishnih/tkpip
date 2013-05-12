#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-06

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, re, logging

# Packages pkg_resources, pip required!
try:
    import pkg_resources, pip
except:
    os.system("{0} {1}".format(sys.executable, "install_pip.py"))
    logging.warning("Restart required!")
    sys.exit(0)

try:
    from .lib.info import __VERSION__
    from .lib.backwardcompat import *
    from .lib.listboxtext import ListBoxText
    from .lib.cache import pipcache
except:
    from lib.info import __VERSION__
    from lib.backwardcompat import *
    from lib.listboxtext import ListBoxText
    from lib.cache import pipcache


# recipe from http://effbot.org/zone/tkinter-menubar.htm
class AppUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("tkPip")

        self.listbox = None
        self.mode = None

        self.status = tk.StringVar()
        self.setStatus()

        self.menubar = tk.Menu(self)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(command=self.onLoadSitePackages, label="Load site packages")
        menu.add_command(command=self.onLoadPipPackages,  label="Load pip packages")
        menu.add_command(command=self.onLoadFile,         label="Load pkglist from file")
        menu.add_separator()
        menu.add_command(command=self.onSaveFile,         label="Save pkglist to file")
        menu.add_separator()
        menu.add_command(command=self.onClear,            label="Clear pkglist")
        menu.add_separator()
        menu.add_command(command=self.quit,               label="Exit")

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Dist", menu=menu)
        menu.add_command(command=self.onInstall,   label="Install")
        menu.add_command(command=self.onUpgrade,   label="Upgrade")
#       menu.add_command(command=self.onUninstall, label="Uninstall")
        menu.add_separator()
        menu.add_command(command=self.onAppend,    label="Append a package")

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Debug", menu=menu)
        menu.add_command(command=self.onPypiCache, label="Pypi Cache")
        menu.add_command(command=self.onPrintData, label="Print Data")

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menu)
        menu.add_command(command=self.onAbout, label="About")

        try:
            self.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.tk.call(master, "config", "-menu", self.menubar)

    def setStatus(self, text=""):
        status = sys.executable
        if text:
            status += " :: " + text
        self.status.set(status)

    def setListbox(self, listbox):
        self.listbox = listbox

    def clearListbox(self):
        if self.listbox:
            self.listbox.clear()

    def onClear(self):
        self.clearListbox()
        self.mode = ""

    def updateMode(self):
        if self.mode == "SitePackages":
            self.onLoadSitePackages()
        elif self.mode == "PipPackages":
            self.onLoadPipPackages()
        self.setStatus()

    def append_item(self, items_dict, key, dist=None):
        if dist:
            active = dist in pkg_resources.WorkingSet()
            version = dist.version
        else:
            active = None
        data = dict(key=key, dist=dist, active=active)
        label = self.get_label(data)
        style = self.get_style(data)
        items_dict[label] = data
        items_dict[label]['_item'] = style

    def get_label(self, data):
        key = data['key']
        active = data['active']
        if active is None:
            label = "{0} [I]".format(key)
        else:
            label = "{0} {1}".format(key, data['dist'].version)
        return label

    def get_style(self, data):
        active = data['active']
        style = {}
        if active is None:
            style = dict(background='Lemonchiffon')
        elif active == False:
            style = dict(background='Gray')
        return style

    def onLoadSitePackages(self):
        self.clearListbox()
        self.mode = "SitePackages"

        if self.listbox:
            distros = pkg_resources.Environment()
            items_dict = {}
            query_list = []
            for key in distros:
                query_list.append(key)
                for dist in distros[key]:
                    self.append_item(items_dict, key, dist)

            self.listbox.insert_items(items_dict)
            self.setStatus("Updating cache...")
            pipcache.query_info(query_list, self.afterUpdate)

    def onLoadPipPackages(self):
        self.clearListbox()
        self.mode = "PipPackages"

        if self.listbox:
            distros = pip.get_installed_distributions()
            items_dict = {}
            query_list = []
            for dist in distros:
                query_list.append(dist.key)
                self.append_item(items_dict, dist.key, dist)

            self.listbox.insert_items(items_dict)
            self.setStatus("Updating cache...")
            pipcache.query_info(query_list, self.afterUpdate)

    def onLoadFile(self):
        self.clearListbox()
        self.mode = ""

        if self.listbox:
            filename = askopenfilename()
            if filename:
                items_dict = {}
                query_list = []

                with open(filename) as f:
                    distros = pkg_resources.Environment()
                    for line in f:
                        line_list = line.split()
                        if line_list:
                            key = line_list[0].lower()
                            if re.match('^[a-z][a-z0-9]*$', key):  # lower_case_with_underscores
                                query_list.append(key)
                                dist = distros[key]
                                dist = dist[0] if dist else None
                                self.append_item(items_dict, key, dist)

                self.listbox.insert_items(items_dict)
                self.setStatus("Updating cache...")
                pipcache.query_info(query_list, self.afterUpdate)

    def afterUpdate(self, *args):
        for i, value, data in self.listbox:
            if value and data:        
                dist = data.get('dist')
                if dist:
                    installed = dist.version
                    name, ver, data, urls, releases = pipcache.get(dist.key)
                    if installed != ver:
                        self.listbox.setValue(i, value + ' [U]')
                        self.listbox.itemconfig(i, dict(background='Lightgreen'))

        self.setStatus()

    def onSaveFile(self):
        if self.listbox:
            filename = asksaveasfilename()
            if filename:
                with open(filename, 'w') as f:
                    for i, value, data in self.listbox:
                        if value:                    
                            f.write("{0}\n".format(value))

    def onActivated(self, event=None):
        self.setStatus("Processing...")
        self.listbox.onActivated()
        self.updateMode()

    def onInstall(self, event=None):
        self.setStatus("Processing...")
        self.listbox.onInstall()
        self.updateMode()

    def onUpgrade(self, event=None):
        self.setStatus("Processing...")
        self.listbox.onUpgrade()
        self.updateMode()

    def onUninstall(self, event=None):
        self.setStatus("Processing...")
#       self.listbox.onUninstall()
        self.updateMode()

    def onAppendPkg(self, event=None):
        pkgname = self.ask_entry1.get().strip()
        self.ask.destroy()
        if pkgname:
            self.setStatus("Processing...")
            self.listbox.pkgInstall(pkgname)
            self.updateMode()

    def onAppend(self, event=None):
        self.ask = tk.Toplevel()
        self.ask.title("Enter a package name")
        self.ask_entry1 = tk.Entry(self.ask)
        self.ask_entry1["width"] = 50
        self.ask_entry1.pack(side=tk.LEFT)
        self.ask_entry1.pack()
        button1 = tk.Button(self.ask, text="Submit", command=self.onAppendPkg)
        button1.pack()
        self.ask_entry1.focus_set()                

    def onPypiCache(self):
        for key, name, ver, data, urls, releases in pipcache:
            print("{0} [{1}]: {2} {3!r}".format(key, name, ver, releases))
            print(repr(data)[:200] + '...')
            print(repr(urls)[:200] + '...')

    def onPrintData(self):
        if self.listbox:
            print(self.listbox._selected)
            for i, value, data in self.listbox:
                print(i, value)
                print(data)

    def onAbout(self):
        print('Version {0}'.format(__VERSION__))


def main():
    root = AppUI()

    # Text Widget
    dFont1 = Font(family="Courier", size=9)
    text1 = tk.Text(root, font=dFont1)
    text1_yscrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=text1.yview)
    text1['yscrollcommand'] = text1_yscrollbar.set

    # Listbox Widget
    listbox1 = ListBoxText(root, text1)
    lb1_yscrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox1.yview)
    listbox1['yscrollcommand'] = lb1_yscrollbar.set

    # Env info
    label1 = tk.Label(root, textvariable=root.status, anchor=tk.W)

    # Bind listbox1 to root
    root.setListbox(listbox1)

    # Grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1, minsize=160)
    root.grid_columnconfigure(1)
    root.grid_columnconfigure(2, weight=3, minsize=400)
    root.grid_columnconfigure(3)
    listbox1.grid(row=0, column=0, sticky='nwes')
    lb1_yscrollbar.grid(row=0, column=1, sticky='nwes')
    text1.grid(row=0, column=2, sticky='nwes')
    text1_yscrollbar.grid(row=0, column=3, sticky='nwes')

    root.grid_rowconfigure(1)
    label1.grid(row=1, column=0, columnspan=4, sticky='nwes')

    # Bind
    listbox1.bind("<ButtonRelease-1>", listbox1.onClicked)
    listbox1.bind("<KeyPress-Up>", listbox1.onClicked)
    listbox1.bind("<KeyPress-Down>", listbox1.onClicked)
    listbox1.bind("<Double-Button-1>", root.onActivated)

    # Main loop
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
