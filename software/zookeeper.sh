#!/bin/bash

ZK_PORT=$1
ZK_ID=$2

INSTALLED=".zookeeper.installed"

if [ -f "$INSTALLED" ]; then
	echo "Zookeeper already installed"
	exit
fi

echo "Installing Zookeeper ..."

wget http://www-eu.apache.org/dist/zookeeper/current/zookeeper-3.4.9.tar.gz
tar -xzf zookeeper-3.4.9.tar.gz
cp -R zookeeper-3.4.9 /srv/zookeeper

cat <<CONFIG >> /srv/zookeeper/conf/zoo.cfg
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/tmp/zookeeper
clientPort=${ZK_PORT}
CONFIG


echo "Adding Zookeeper upstart ..."

cat <<UPSTART >> /etc/init/zookeeper.conf
description "Service for Zookeeper"
author      "Kyle Bush"

start on filesystem or runlevel [2345]
stop on shutdown

script

    echo $$ > /var/run/zookeeper.pid
    exec /srv/zookeeper/bin/zkServer.sh start

end script

pre-start script
    echo "[`date`] Zookeeper starting" >> /var/log/zookeeper.log
end script

pre-stop script
    rm /var/run/zookeeper.pid
    echo "[`date`] Zookeeper stopping" >> /var/log/zookeeper.log
end script
UPSTART

init-checkconf /etc/init/zookeeper.conf
sudo service zookeeper start
echo "Zookeeper installed and started."
touch $INSTALLED

