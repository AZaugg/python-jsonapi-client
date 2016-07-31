import os
import json
from jsonapiclient import JSONAPIClient


def get_wrapper(self, url):
    url = url.replace('/', '_')
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), url)
    print path
    return json.loads(open(path).read())

JSONAPIClient._get = get_wrapper


def test_basic_jsonapiclient():
    api = JSONAPIClient('')
    assert api.url == ''
    Hive = api.Collection('hive')
    assert Hive.name == 'hive'
    assert Hive.url == 'hive'

    hive_one = Hive.get(1)
    assert hive_one.id == '1'

    hive_one_bees = hive_one.bees
    assert isinstance(hive_one.bees, list)
    assert hive_one_bees[0].id == '1'
    assert hive_one_bees[1].id == '2'
