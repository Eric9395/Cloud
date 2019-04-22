#!/usr/bin/env bash
ansible-playbook -i hosts -u ubuntu --key-file=testKeypair.pem playbook.yml
