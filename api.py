#!/usr/bin/env python
import requests

default_headers = {'accept': 'application/vnd.api+json'}


def json_get(url):
    response = requests.get(url, headers=default_headers)
    return response


class API(object):
    def __init__(self, url):
        self.url = url

    def __getattr__(self, args):
        try:
            return self.__getattribute__(args)
        except Exception:
            pass

        url = self.url + args

        response = json_get(url)
        json_response = response.json()
        if response.status_code == 200:
            collection = Collection(self, args, json_response)
            setattr(self, args, collection)
            return collection

        return self.__getattribute__(args)

    def get(self, url):
        response = requests.get(url, headers=default_headers)
        json_response = response.json()
        return json_response


class Collection(object):
    def __init__(self, api, name, json_response={}):
        self.api = api
        self.name = name
        self.resources = []
        for resource_data in json_response.get('data', {}):
            resource_id = resource_data.get('id')
            r = Resource(self, name, resource_id, resource_data)
            self.resources.append(r)

    def get(self, resource_id):
        url = '{0}{1}/{2}'.format(self.api.url, self.name, resource_id)
        resource_data = self.api.get(url).get('data', {})
        resource_id = resource_data.get('id')
        return Resource(self.api, self.name, resource_id, resource_data)


class Resource(object):
    def __init__(self, api, collection, resource_id, json_response={}):
        self.api = api
        self.collection = collection
        self.resource_id = resource_id
        self.url = json_response.get('links', {}).get('self')
        self._keys = []
        self.attributes = json_response.get('attributes', {})
        for attr_key, attr_value in self.attributes.items():
            self._keys.append(attr_key)
            setattr(self, attr_key, attr_value)

        for x in json_response.get('relationships', {}).values():
            for relationship_data in x.get('data', []):
                if not isinstance(relationship_data, dict):
                    continue

                r_type = relationship_data.get('type')
                r_id = relationship_data.get('id')
                r_types = '{0}s'.format(r_type)

                if not hasattr(self, r_types):
                    setattr(self, r_types, [])

                v = getattr(self, r_types)

                r = Resource(
                    self.api,
                    r_type,
                    r_id,
                    {}
                )
                v.append(r)
                setattr(self, r_types, v)

    def __repr__(self):
        return "<Resource {0.collection}:{0.resource_id}>".format(self)

    def keys(self):
        return self._keys


if __name__ == '__main__':
    api = API('http://localhost:5000/api/')
    print "hive1  :", api.hive.get(1)
    print "bee2   :", api.bee.get(2)
    print "h.bees :", api.hive.get(1).bees
    print "bee2   :", api.bee.get(1)
