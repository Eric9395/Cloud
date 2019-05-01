#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook --ask-become-pass playbook.yml
