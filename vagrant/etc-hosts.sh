#!/bin/bash

IP=$1
HOSTNAME=$2

ENTRY="$IP $HOSTNAME"

#sudo sed -i.bu "/^127.0.1.1/d" /etc/hosts
sudo sed -i.bu "/^${IP}/d" /etc/hosts
echo "$ENTRY" | sudo tee -a /etc/hosts
