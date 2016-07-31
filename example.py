from jsonapiclient import JSONAPIClient


api = JSONAPIClient('http://localhost:5000/api/')
Hive = api.Collection('hive')
print Hive.all()
