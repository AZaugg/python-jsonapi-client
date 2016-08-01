from jsonapiclient import JSONAPIClient
from utils import get_wrapper

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
