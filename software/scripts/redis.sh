#!/bin/bash

REDIS_VERSION=$1
REDIS_PORT=$2
REDIS_DATA_DIR=$3

CONFIG_FILE=/etc/redis/${REDIS_PORT}.conf
LOG_FILE=/var/log/redis_${REDIS_PORT}.log
DATA_DIR=${REDIS_DATA_DIR}/${REDIS_PORT}
EXECUTABLE=/usr/local/bin/redis-server

INSTALLED=".redis.installed"

if [ -f "$INSTALLED" ]; then
	echo "Redis already installed"
	exit
fi

echo "Installing Redis $REDIS_VERSION ..."

sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

sudo apt-get -y install build-essential tcl8.5 make gcc
wget http://download.redis.io/releases/redis-${REDIS_VERSION}.tar.gz -O ~/redis.tgz

sudo mkdir -p /srv/redis
cd /srv/redis
sudo tar -xvzf ~/redis.tgz --strip 1

cd deps
sudo make hiredis jemalloc linenoise lua
cd ..
sudo make install

echo -e \
  "$REDIS_PORT\n$CONFIG_FILE\n$LOG_FILE\n$DATA_DIR\n$EXECUTABLE\n" | \
  sudo utils/install_server.sh

echo "## ---- CUSTOM CONFIGURATION ---" | sudo tee -a ${CONFIG_FILE}
echo "bind 0.0.0.0" | sudo tee -a ${CONFIG_FILE}

sudo service redis_${REDIS_PORT} restart

touch ~/${INSTALLED}

