from jsonapiclient import JSONAPIClient


def test_basic_resource():
    api = JSONAPIClient('http://localhost:5000/api/')
    Hive = api.Collection('hive')
    assert Hive.name == 'hive'
    assert Hive.url == 'http://localhost:5000/api/hive'
    assert str(Hive) == '<Collection Hive>'

    hive_one = Hive.get(1)
    assert hive_one.url == 'http://localhost:5000/api/hive/1'
    assert str(hive_one) == '<Hive:1>'


def test_resource_short_url():
    hive = JSONAPIClient('http://localhost:5000/api/').Collection('hive').get(1)
    assert hive.short_url() == 'hive/1'


def test_resource_keys():
    hive = JSONAPIClient('http://localhost:5000/api/').Collection('hive').get(1)
    assert list(hive.keys()) == ['location']


def test_resource_self_url():
    hive = JSONAPIClient('http://localhost:5000/api/').Collection('hive').get(1)
    assert hive.self_url() == 'http://localhost:5000/api/hive/1'
