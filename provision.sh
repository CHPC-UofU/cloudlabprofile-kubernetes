#!/bin/bash

# Enable strict mode:
set -euo pipefail

# Variables:
export ANSIBLE_VERBOSITY=1

cd ./playbooks
ansible-playbook -v -i ./inventory/hosts.yml ./prerequisites.yml