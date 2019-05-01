# Main Code: /deployment

docker swarm join --token SWMTKN-1-3byvgi7l73b0htxywqh9z7m4yrh2wneagaqws7oxjdkr5epzbu-69mv6ynr1uec1mj8sht2au1us 45.113.233.94:2377


sudo docker swarm init
sudo docker node ls
sudo docker stack deploy -c docker-compose.yml node0compose
sudo docker service ls
sudo docker service ps node0compose_web
sudo docker stack services node0compose
sudo docker container ls -q
sudo curl -4 http://localhost:80
sudo docker service scale node0compose_web=3
