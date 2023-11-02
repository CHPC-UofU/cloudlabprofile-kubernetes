#!/bin/bash

# Enable strict mode:
set -euo pipefail

# Variables:
export ANSIBLE_VERBOSITY=2

cd ./playbooks
ansible-playbook -i ./inventory/hosts.yml ./prerequisites.yml