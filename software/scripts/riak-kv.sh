#!/usr/bin/env bash

INSTALLED=".riak-kv.installed"

if [ -f "$INSTALLED" ]; then
	echo "Riak KV already installed"
	exit
fi

echo "Installing Riak KV ..."
curl https://packagecloud.io/gpg.key | sudo apt-key add -

sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

sudo apt-get -y install apt-transport-https

HOSTNAME=`hostname -f`
FILENAME=/etc/apt/sources.list.d/basho.list
OS=ubuntu
DIST=trusty
PACKAGE_CLOUD_RIAK_DIR=https://packagecloud.io/install/repositories/basho/riak
sudo curl "$PACKAGE_CLOUD_RIAK_DIR/config_file.list?os=$OS&dist=$DIST&name=$HOSTNAME" > ${FILENAME}

sudo apt-get -y update
sudo apt-get -y install riak
sudo riak start

touch ~/${INSTALLED}
