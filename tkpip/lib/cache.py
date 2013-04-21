#!/usr/bin/env python
# coding=utf-8
# Stan 2013-04-20

import threading, logging
import pip
from pip.backwardcompat import xmlrpclib


# For updating information about packages from PyPI


class Cache(object):
    def __init__(self, query=[]):
        self.index_url = 'http://pypi.python.org/pypi'
        self.pypi = xmlrpclib.ServerProxy(self.index_url, pip.download.xmlrpclib_transport)
        self.pypi_cache = {}
        self.query = query
        self.t = None

        if self.query:
            self.query_info(self.query)

    def __iter__(self):
        for key in self.pypi_cache:
            name, ver, data, urls, releases = self.pypi_cache[key]
            yield key, name, ver, data, urls, releases

    def get(self, key):
        value = self.pypi_cache.get(key)
        if value:
            name, ver, data, urls, releases = value
        else:
            name, ver, data, urls, releases = None, None, {}, [], []
        return name, ver, data, urls, releases

    def query_info(self, query, after_func=None):
        if self.t and self.t.isAlive():
            logging.warning('Query is processing, new query skipped!')
            return
        self.t = threading.Thread(target=self.t_func, args=(self.cache_info, after_func, query))
        self.t.daemon = True
        self.t.start()

    def t_func(self, func, after_func, *args):
        func(*args)
        if after_func:
            after_func(*args)

    def cache_info(self, query):
        if isinstance(query, list):
            for query in query:
                self.cache_info(query)
            return
        elif query in self.pypi_cache:
            return

        releases = self.pypi.package_releases(query)

        # package_releases() method is case-sensitive,
        # if nothing found then we search for it
        if not releases:
            for item in self.pypi.search({'name': query}):
                if query.lower() == item['name'].lower():
                    query = item['name']
                    break
            else:
                logger.info("No packages found matching {}".format(query))
                self.pypi_cache[query] = 'No found', {}, [], []

            releases = self.pypi.package_releases(query)

        ver = releases[0] if releases else 'No info'
        data = self.pypi.release_data(query, ver) if ver else {}
        urls = self.pypi.release_urls(query, ver) if ver else []

        self.pypi_cache[query.lower()] = query, ver, data, urls, releases
