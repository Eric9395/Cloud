#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=testKeypair.pem docker_install.yml
