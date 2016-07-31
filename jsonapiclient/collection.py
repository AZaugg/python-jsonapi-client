#!/usr/bin/env python
# from api import JSONAPIClient
from jsonapiobject import JSONAPIObject
import resource
import jsonapi


class Collection(JSONAPIObject):
    def __init__(self, url, api=None):
        collection_type = url.split('/')[-1]
        base_url = url.split(collection_type)[0]

        self.name = collection_type
        self.type = collection_type
        self.url = url
        if not api:
            api = jsonapi.JSONAPIClient(url=base_url)
        self.api = api
        self.resources = []

    def all(self, disable_cache=False):
        json_response = self.api.get(self.url)
        for resource_json in json_response.get('data', {}):
            resource_id = resource_json.get('id')
            r = resource.Resource(self.type, resource_id, resource_json, self)
            self.resources.append(r)
        return self.resources

    def get(self, resource_id, disable_cache=False):
        url = '{0}{1}/{2}'.format(self.api.url, self.name, resource_id)
        resource_json = self.api.get(url).get('data', {})
        resource_id = resource_json.get('id')

        return resource.Resource(
            resource_type=self.type, resource_id=resource_id,
            resource_json=resource_json, collection=self)

    def __str__(self):
        return "<Collection {0}>".format(self.type.title())
