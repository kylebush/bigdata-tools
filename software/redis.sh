#!/bin/bash

REDIS_VERSION=$1
REDIS_PORT=$2

CONFIG_FILE=/etc/redis/$REDIS_PORT.conf
LOG_FILE=/var/log/redis_$REDIS_PORT.log
DATA_DIR=/var/lib/redis/$REDIS_PORT
EXECUTABLE=/usr/local/bin/redis-server

INSTALLED=".redis.installed"

if [ -f "$INSTALLED" ]; then
	echo "Redis already installed"
	exit
fi

echo "Installing Redis ${REDIS_VERSION} ..."

sudo apt-get update
sudo apt-get install build-essential tcl8.5 make gcc
sudo wget http://download.redis.io/releases/redis-$REDIS_VERSION.tar.gz
sudo tar xzf redis-$REDIS_VERSION.tar.gz
cd redis-$REDIS_VERSION
cd deps
sudo make hiredis jemalloc linenoise lua
cd ..
sudo make install

echo -e \
  "${REDIS_PORT}\n${CONFIG_FILE}\n${LOG_FILE}\n${DATA_DIR}\n${EXECUTABLE}\n" | \
  sudo utils/install_server.sh

echo -e "\nbind 0.0.0.0\n" >> $CONFIG_FILE

sudo service redis_$REDIS_PORT restart

touch $INSTALLED