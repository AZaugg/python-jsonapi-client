#!/usr/bin/env python
from jsonapiobject import JSONAPIObject


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
