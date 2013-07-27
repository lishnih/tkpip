#!/usr/bin/env python
# coding=utf-8
# Stan 2012-10-03

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, tempfile, logging

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse


def step_1():
    logging.info("Checking Setuptools/Distribute")
    try:
        import setuptools
        logging.info("Setuptools/Distribute installed!")
    except ImportError:
        logging.info("Installing Setuptools...")

        url = "https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py"
        dtemp = tempfile.mkdtemp()
        filename = download_file(url, dtemp)
        os.system("{0} {1}".format(sys.executable, filename))


def step_2():
    logging.info("Checking Pip")
    try:
        import pip
        logging.info("Pip installed!")
    except ImportError:
        logging.info("Installing Pip...")

        from pkg_resources import load_entry_point
        packages_list = [
            'pip',
        ]
        install_func = load_entry_point('setuptools', 'console_scripts', 'easy_install')
        return install_func(packages_list)


#recipe from http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
def download_file(url, desc=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    step = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    func_name = 'step_{0}'.format(step)
    f = globals()[func_name] if func_name in globals() else None

    if f:
        logging.info("=== Step {0} ===".format(step))
        res = f()
        os.system("{0} {1} {2}".format(sys.executable,
            os.path.basename(__file__), step+1))
