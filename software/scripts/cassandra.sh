#!/bin/bash

INSTALLED=".cassandra.installed"

if [ -f "$INSTALLED" ]; then
	echo "Cassandra already installed"
	exit
fi

echo "Installing Cassandra ..."

echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
sudo apt-get -y install cassandra

touch ~/${INSTALLED}

sudo pkill -f CassandraDaemon

sudo service cassandra start

