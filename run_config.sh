#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook -i hosts docker_install.yml
