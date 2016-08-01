import os
import json


def get_wrapper(self, url):
    url = url.replace('/', '_')
    url = url.replace('http:__localhost:5000_api_', '')
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), url)
    return json.loads(open(path).read())
