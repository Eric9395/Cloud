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

curl http://Admin:admin@0.0.0.0:5984/_membership

curl -X GET 0.0.0.0:5984/test

curl -X GET 103.6d.254.63:5984/test

curl http://0.0.0.0:5984/_uuids?count=2
ip:5984/_utils
curl -X PUT http://0.0.0.0:5984/test -u "Admin:admin"

curl -X PUT http://0.0.0.0:5999/test2 -u "Admin:admin"

curl -X POST -d '{"todo":"task 1", "done":false}' http://0.0.0.0:5984/test -H "Content-Type:application/json"

curl -X POST -d '{"_id":"test1", "todo":"task 2", "done":false}' http://0.0.0.0:5984/test -H "Content-Type:application/json"

curl -X POST -d '{"docs": [{"todo":"task 3", "done":false}, {"todo":"task 4", "done":false}]}' http://0.0.0.0:5984/test/_bulk_docs -H "Content-Type:application/json"


CouchDB:
/opt/couchdb/etc/local.d/docker.ini

Shards and Replicas: https://docs.couchdb.org/en/master/cluster/sharding.html
