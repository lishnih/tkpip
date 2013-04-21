#!/usr/bin/env python
# coding=utf-8
# Stan 2012-10-03

import sys, os, tempfile, logging
try:    import urllib2
except: import urllib.request as urllib2


def step_1():
    logging.info("Installing Distribute")
    try:
        import pkg_resources
        logging.info("Distribute already installed!")
    except:
        logging.info("Installing Distribute...")

        url = "http://python-distribute.org/distribute_setup.py"
        dtemp = tempfile.mkdtemp()
        filename = download_file(url, dtemp)
        os.system("{} {}".format(sys.executable, filename))


def step_2():
    logging.info("Installing Pip")
    try:
        import pip
        logging.info("Pip already installed!")
    except:
        logging.info("Installing Pip...")

        from pkg_resources import load_entry_point
        packages_list = [
            'pip',
        ]
        install_func = load_entry_point('distribute', 'console_scripts', 'easy_install')
        return install_func(packages_list)


#recipe from http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
def download_file(url, desc=None):
    u = urllib2.urlopen(url)
    filename = url.split('/')[-1]
    if not filename:
        filename = 'file.dat'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        file_size = int(meta_func("Content-Length")[0])
        logging.info("Downloading: %s Bytes: %s" % (url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print(status),

    return filename


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    step = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    func_name = 'step_{}'.format(step)
    f = globals()[func_name] if func_name in globals() else None

    if f:
        logging.info("=== Step {} ===".format(step))
        res = f()
        os.system("{} {} {}".format(sys.executable,
                                    os.path.basename(__file__),
                                    step+1))
