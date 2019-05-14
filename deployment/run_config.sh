#!/usr/bin/env bash

# Team 20
# Team member: Site Huang, 908282
#              Chenyuan Zhang, 815901
#              Zixuan Zhang, 846305
#              Zhentao Zhang, 864735
#              Kangyun Dou, 740145

. ./openrc.sh; ansible-playbook -i hosts docker_install.yml
