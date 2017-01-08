#!/bin/bash

IP=$1
MACHINE=$2
VAGRANT_DIRECTORY="${PWD%/*}"

TAG="### Vagrant - ${MACHINE}"

sed -i -n "/$TAG/,/$TAG/d" ~/.ssh/config

cat >> ~/.ssh/config << EOF
${TAG}
Host ${MACHINE}
  HostName ${IP}
  User vagrant
  Port 22
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile "${VAGRANT_DIRECTORY}/vagrant/.vagrant/machines/${MACHINE}/virtualbox/private_key"
  IdentitiesOnly yes
  LogLevel INFO
${TAG}

EOF





