from jsonapiclient import JSONAPIClient


def test_basic_collection():
    api = JSONAPIClient('')
    Hive = api.Collection('hive')
    assert Hive.name == 'hive'
    assert Hive.url == 'hive'
    assert str(Hive) == '<Collection Hive>'


def test_collection_all():
    api = JSONAPIClient('')
    Hive = api.Collection('hive')
    all_hives = Hive.all()
    assert isinstance(all_hives, list)
