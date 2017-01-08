#!/bin/bash

VERSION=$1
ZK_PORT=$2
ZK_ID=$3
ZK_NODES=`(echo $4 | tr ',' '\n')`

INSTALLED=".zookeeper.installed"

if [ -f "$INSTALLED" ]; then
	echo "Zookeeper already installed"
	exit
fi

echo "Installing Zookeeper ..."

sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

sudo apt-get -y install zookeeperd

sudo cat <<CONFIG >> /srv/zookeeper/conf/zoo.cfg
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper
clientPort=$ZK_PORT
$ZK_NODES
CONFIG

sudo service zookeeper restart
echo "Zookeeper installed and started."
touch ~/${INSTALLED}

