#!/bin/bash

HOST=$1

INSTALLED=".cassandra.installed"

if [ -f "$INSTALLED" ]; then
	echo "Cassandra already installed"
	exit
fi

echo "Installing Cassandra ..."

echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
sudo apt-get update -y
sudo apt-get install cassandra -y

sudo sed -i.bu "s/127.0.0.1/${HOST}/g" /etc/cassandra/cassandra.yaml
sudo sed -i.bu "s/localhost/${HOST}/g" /etc/cassandra/cassandra.yaml

sudo pkill -9 java

touch $INSTALLED

sudo service cassandra start

