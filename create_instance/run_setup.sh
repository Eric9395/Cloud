#!/usr/bin/env bash
. ./create_instance1/openrc.sh; ansible-playbook --ask-become-pass create_instance1/playbook.yml create_instance2/playbook.yml
