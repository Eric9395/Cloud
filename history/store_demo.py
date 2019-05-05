import couchdb
couchdb_username = 'Admin'
couchdb_password = 'admin'
server = couchdb.Server(url='http://'+couchdb_username+':'+couchdb_password+'@127.0.0.1:5984/')
try:
    db = server['demo1']
except couchdb.http.ResourceNotFound as e:
    server.create('demo1')
    db = server['demo1']
a = {'a':1,'b':2}
db.save(a)
