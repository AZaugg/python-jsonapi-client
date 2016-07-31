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


Getting a Hive object with the id of 1
```
>>> api = API('http://localhost:5000/api/')
>>> api.hive.get(1)
<Resource hive:1>
```

Getting the url of the first Hive object
```
>>> api.hive.get(1).url
http://localhost:5000/api/hive/1
```

Get all the attributes for a  Hive
```
>>> api.hive.get(1).attributes
{u'location': u'backyard'}
```

Get all the keys for a hive
```
>>> api.hive.get(1).keys()
[u'location']
```

Get all the Bees in a hive

```
[bee for bee in api.hive.get(1).bees]
[<Resource bee:1>, <Resource bee:2>]
```

Get a bee's name
```
>>> api.bee.get(1).name
u'adam'
```
	

