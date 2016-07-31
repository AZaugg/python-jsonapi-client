#!/usr/bin/env python
import logging
import requests

import collection
# from collection import Collection

default_headers = {'accept': 'application/vnd.api+json'}


class JSONAPIClient(object):
    def __init__(self, url):
        self.url = url
        self.resources = []
        self._cache = {}

    def get(self, url):
        hit = self._cache.get(url)
        if hit:
            return hit
        miss = self._get(url)
        self._cache[url] = miss
        return miss

    def _get(self, url):
        logging.debug("GET:{0}:{1}".format(id(self), url))
        response = requests.get(url, headers=default_headers)
        json_response = response.json()
        return json_response

    def Collection(self, collection_name):
        url = "{0}{1}".format(self.url, collection_name)
        return collection.Collection(url, self)
