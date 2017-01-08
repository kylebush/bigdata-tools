#!/bin/bash

VERSION=$1

INSTALLED=".kafka.installed"

if [ -f "$INSTALLED" ]; then
	echo "Kafka already installed"
	exit
fi

echo "Installing Kafka ..."

wget http://www-eu.apache.org/dist/kafka/$VERSION/kafka_2.11-$VERSION.tgz -O ~/kafka.tgz

sudo mkdir -p /srv/kafka
cd /srv/kafka
sudo tar -xvzf ~/kafka.tgz --strip 1

echo "Adding Kafka upstart ..."

sudo cat <<UPSTART >> /etc/init/kafka.conf
description "Service for Kafka"
author      "Kyle Bush"

start on filesystem or runlevel [2345]
stop on shutdown

script

    echo \$\$ > /var/run/kafka.pid
    exec /srv/kafka/bin/kafka-server-start.sh /srv/kafka/config/server.properties >> /var/log/kafka.log

end script

pre-start script
    echo "[`date`] Kafka starting" >> /var/log/kafka.log
end script

pre-stop script
    rm /var/run/kafka.pid
    echo "[`date`] Kafka stopping" >> /var/log/kafka.log
end script
UPSTART

sudo init-checkconf /etc/init/kafka.conf
sudo service kafka start

echo "Kafka installed and started."
touch ~/${INSTALLED}

