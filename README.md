# COMP90024 - Cluster and Cloud Computing - Project
# _A Cloud System comprising of CouchDB Cluster, Twitter Harvester, and Web Server_
_Twitter API, Docker, CouchDB Cluster, Django Web_.

## Files
- **Harvester and Analyzer**: contains the implementation of Twitter crawler, model analyzer for sentimental analysis.
- **create_instance**: contains the ansible playbook for automatically creating instances on Nectar Cloud Platform.
- **deployment**: contains the ansible execution playbook and docker setup files (Dockerfile, docker-compose) for installing packages and deploying the CouchDB cluster and web servers among all nodes. The front-end wep application is in this directory as well, which is written in Python and JavaScript based on the Django web frameworks.

## How to execute
### Create instances
To create instances on Nectar, we need to run the shell file run-nectar.sh. The command is "sh run-nectar".
As long as all the dependacies illustrated in the report are installed, the code should be able to run and then just wait 7 to 8 minutes until the process finished.

### Deployment
- Running "./run_config.sh"
- This process takes about 10 mins to setup the Cloud system. 
- hosts: A list of nodes IP addressses and vars
- roles: Ansible playbook execution tasks
- docker_install.yml: The main entrance of the ansible playbook code.
