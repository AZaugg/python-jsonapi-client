#!/usr/bin/env python


default_headers = {'accept': 'application/vnd.api+json'}


class JSONAPIObject(object):

    def short_url(self):
        print self.api.url
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
        from .resource import Resource

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
