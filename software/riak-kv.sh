#!/usr/bin/env bash

INSTALLED=".riak-kv.installed"

if [ -f "$INSTALLED" ]; then
	echo "Riak KV already installed"
	exit
fi

echo "Installing Riak KV ..."
curl https://packagecloud.io/gpg.key | sudo apt-key add -
sudo apt-get install -y apt-transport-https

HOSTNAME=`hostname -f`
FILENAME=/etc/apt/sources.list.d/basho.list
OS=ubuntu
DIST=trusty
PACKAGE_CLOUD_RIAK_DIR=https://packagecloud.io/install/repositories/basho/riak
curl "${PACKAGE_CLOUD_RIAK_DIR}/config_file.list?os=${OS}&dist=${DIST}&name=${HOSTNAME}" > $FILENAME


sudo apt-get update
sudo apt-get install riak
sudo riak start

touch $INSTALLED
