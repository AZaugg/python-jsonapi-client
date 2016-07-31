#!/usr/bin/env python
import requests
import logging

default_headers = {'accept': 'application/vnd.api+json'}


class API(object):
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
        return Collection(url, self)


class JSONAPIObject(object):

    def short_url(self):
        return self.url.replace(self.api.url, '')

    def keys(self):
        return self.attributes.keys()

    def set_links(self, json_data={}):
        if json_data == {} and self.json_data == {}:
            self_url = self.self_url()
            self.json_data = self.api.get(self_url)

        self.url = json_data.get('links', {}).get('self')
        return self.url

    def self_url(self):
        return "{0}{1}/{2}".format(self.api.url, self.type, self.id)

    def set_attributes(self, json_data={}):

        if json_data == {} and self.json_data == {}:
            self_url = self.self_url()
            json_data = self.api.get(self_url)
            self.json_data = json_data

        assert isinstance(json_data, dict)
        attributes = json_data.get('attributes', {})
        self.attributes = attributes

        if not hasattr(self, 'keys'):
            self.keys = []

        for attr_key, attr_value in attributes.items():
            setattr(self, attr_key, attr_value)

        return attributes

    def set_relationships(self, json_data={}):
        if json_data == {} and self.json_data == {}:
            self_url = self.self_url()
            json_data = self.api.get(self_url)
            self.json_data = json_data

        resources = []
        relationships = json_data.get('relationships', {}).items()
        for collection_name, resource_data in relationships:
            e = resource_data.get('data', [])

            if not isinstance(e, list):
                e = [e]

            for relationship_data in e:
                resource_type = relationship_data.get('type')
                resource_id = relationship_data.get('id')

                r = Resource(
                    resource_type=resource_type,
                    resource_id=resource_id,
                    resource_json={},
                    collection=self.collection
                )
                resources.append(r)
            setattr(self, collection_name, resources)
        return resources


class Collection(JSONAPIObject):
    def __init__(self, url, api=None):
        collection_type = url.split('/')[-1]
        base_url = url.split(collection_type)[0]

        self.name = collection_type
        self.type = collection_type
        self.url = url
        if not api:
            api = API(url=base_url)
        self.api = api
        self.resources = []

    def all(self, disable_cache=False):
        json_response = self.api.get(self.url)
        for resource_json in json_response.get('data', {}):
            resource_id = resource_json.get('id')
            r = Resource(self.type, resource_id, resource_json, self)
            self.resources.append(r)
        return self.resources

    def get(self, resource_id, disable_cache=False):
        url = '{0}{1}/{2}'.format(self.api.url, self.name, resource_id)
        resource_json = self.api.get(url).get('data', {})
        resource_id = resource_json.get('id')

        return Resource(resource_type=self.type, resource_id=resource_id,
                        resource_json=resource_json, collection=self)

    def __str__(self):
        return "<Collection {0}>".format(self.type.title())


class Resource(JSONAPIObject):

    def __init__(self, resource_type, resource_id, resource_json,
                 collection=None):
        self.id = resource_id
        self.type = resource_type
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.json_data = resource_json

        if collection:
            self.collection = collection
            self.api = collection.api

        self.set_attributes(resource_json)
        self.set_links(resource_json)
        self.set_relationships(resource_json)

    def __repr__(self):
        return "<{0}:{1}>".format(self.type.title(), self.id)


if __name__ == '__main__':
    api = API('http://localhost:5000/api/')
    Hive = api.Collection('hive')

    print "All Hives:        ", Hive.all()
    print "Hive 1 url:       ", Hive.get(1).url
    print "Hive 1 location:  ", Hive.get(1).location
    print "Hive 1 attributes:", Hive.get(1).attributes
    print "Hive 1 bees:      ", Hive.get(1).bees

    Bee = Collection('http://localhost:5000/api/bee', api)
    print "All Bees:         ", Bee.all()
