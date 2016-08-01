[![Build Status](https://travis-ci.org/daniellawrence/python-jsonapi-client.svg?branch=master)](https://travis-ci.org/daniellawrence/python-jsonapi-client)

jsonapi-client for python
-------------------------------

Small and silly jsonapi-client for python powered by requests.


Examples
----------

All the examples are based on the following SQLAlchemy running JSONAPI on http://localhost:5000

```
class Hive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)

class Bee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    hive_id = db.Column(db.Integer, db.ForeignKey('hive.id'))
    hive = db.relationship('Hive', backref=db.backref('bees', lazy='dynamic'))
```


Getting all the Hives
```
>>> api = JSONAPIClient('http://localhost:5000/api/')
>>> Hive = api.Collection('hive')
>>> Hive.all()
[<Hive:1>]
```

Getting Hive with the ID of 1
```
>>> Hive.get(1).url
http://localhost:5000/api/hive/1
```

Get all the attributes for a  Hive
```
>>> Hive.get(1).attributes
{u'location': u'backyard'}
```

Get all the keys for a hive
```
>>> Hive.get(1).keys()
[u'location']
```

Get all the Bees in a hive

```
>>> api.hive.get(1).bees
[<Bee:1>, <Bee:2>]
```

Create a new collection 'Bee'
```
>>> api = JSONAPIClient('http://localhost:5000/api/')
>>> Bee = Collection('http://localhost:5000/api/bee', api)
>>> Bee.all()
[<Bee:1>, <Bee2:>]
```

Get a bee's name
```
>>> api.bee.get(1).name
u'adam'
```

TODO
-----

lots
