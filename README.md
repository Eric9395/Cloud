# Main Code: /deployment


sudo docker swarm init
sudo docker node ls
sudo docker stack deploy -c docker-compose.yml node0
sudo docker service ls
sudo docker service ps node0compose_web
sudo docker stack services node0compose
sudo docker container ls -q
sudo curl -4 http://localhost:80
sudo docker service scale node0compose_web=3

# Error response from daemon: rpc error: code = Unknown desc = The swarm does not have a leader. It's possible that too few managers are online. Make sure more than half of the managers are online.
sudo docker swarm init --force-new-cluster

sudo docker inspect ID

sudo docker cp containerID:container_path host_path

# enter in docker
sudo docker exec -it ID bash


curl -X POST -H "Content-Type: application/json" http://Admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "Admin", "password":"admin", "node_count":"2"}'


curl -X POST -H "Content-Type: application/json" http://Admin:admin@45.113.233.94:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "Admin", "password":"admin", "port": 5984, "node_count": "3", "remote_node": "103.6.254.26", "remote_current_user": "Admin", "remote_current_password": "admin" }'
curl -X POST -H "Content-Type: application/json" http://Admin:admin@45.113.233.94:5984/_cluster_setup -d '{"action": "add_node", "host":"103.6.254.26", "port": 5984, "username": "Admin", "password":"admin"}'


curl -X POST -H "Content-Type: application/json" http://Admin:admin@45.113.233.94:5984/_cluster_setup -d '{"action": "finish_cluster"}'

curl http://Admin:admin@45.113.233.94:5984/_cluster_setup


# First, get two UUIDs to use later on. Be sure to use the SAME UUIDs on all nodes.
curl http://45.113.233.94:5984/_uuids?count=2

# CouchDB will respond with something like:
#   {"uuids":["60c9e8234dfba3e2fdab04bf92001142","60c9e8234dfba3e2fdab04bf92001cc2"]}
# Copy the provided UUIDs into your clipboard or a text editor for later use.
# Use the first UUID as the cluster UUID.
# Use the second UUID as the cluster shared http secret.

# Create the admin user and password:
curl -X PUT http://<server-IP|FQDN>:5984/_node/_local/_config/admins/admin -d '"password"'

curl -X PUT http://45.113.233.94:5984/_node/_local/_config/admins/admin -d 'mysecretpassword'

# Now, bind the clustered interface to all IP addresses availble on this machine
curl -X PUT http://127.0.0.1:5984/_node/_local/_config/chttpd/bind_address -d '"0.0.0.0"' -u "Admin:admin"

# Set the UUID of the node to the first UUID you previously obtained:
curl -X PUT http://127.0.0.1:5984/_node/_local/_config/couchdb/uuid -d '"4fc84787514deb6a88801d74b6000b1b"' -u "Admin:admin"

# Finally, set the shared http secret for cookie creation to the second UUID:
curl -X PUT http://127.0.0.1:5984/_node/_local/_config/couch_httpd_auth/secret -d '"4fc84787514deb6a88801d74b6000e7f"' -u "Admin:admin"




curl http://Admin:admin@0.0.0.0:5984/_membership

curl -X GET 0.0.0.0:5984/_membership -u "Admin:admin"

curl -X GET 0.0.0.0:5984/test



curl -X GET 103.6d.254.63:5984/test

curl http://0.0.0.0:5984/_uuids?count=2
ip:5984/_utils
curl -X PUT http://0.0.0.0:5984/test -u "Admin:admin"

curl -X PUT http://0.0.0.0:5984/test2 -u "Admin:admin"

curl -X POST -d '{"todo":"task 1", "done":false}' http://45.113.233.94:5984/test -H "Content-Type:application/json"

curl -X POST -d '{"_id":"intest", "todo":"task 2", "done":false}' http://45.113.233.94:5984/test -H "Content-Type:application/json"

curl -X POST -d '{"docs": [{"todo":"task 3", "done":false}, {"todo":"task 4", "done":false}]}' http://0.0.0.0:5984/test/_bulk_docs -H "Content-Type:application/json"


CouchDB:
/opt/couchdb/etc/local.d/docker.ini

Shards and Replicas: https://docs.couchdb.org/en/master/cluster/sharding.html





curl -X POST -H "Content-Type: application/json" http://Admin:admin@103.6.254.16:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "Admin", "password":"admin", "port": 5984, "node_count": "3", "remote_node": "103.6.254.41", "remote_current_user": "Admin", "remote_current_password": "admin" }'
curl -X POST -H "Content-Type: application/json" http://Admin:admin@103.6.254.16:5984/_cluster_setup -d '{"action": "add_node", "host":"103.6.254.41", "port": 5984, "username": "Admin", "password":"admin"}'
