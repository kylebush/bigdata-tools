#!/bin/bash

INSTALLED=".kafka.installed"

if [ -f "$INSTALLED" ]; then
	echo "Kafka already installed"
	exit
fi

echo "Installing Kafka broker..."

wget http://www-eu.apache.org/dist/kafka/0.10.1.0/kafka_2.11-0.10.1.0.tgz

tar -xzf kafka_2.11-0.10.1.0.tgz
cp -R kafka_2.11-0.10.1.0 /srv/kafka

cat <<CONFIG >> /srv/kafka/config/server.properties
CONFIG


echo "Adding Kafka upstart ..."

cat <<UPSTART >> /etc/init/kakfa.conf
description "Service for Kafka"
author      "Kyle Bush"

start on filesystem or runlevel [2345]
stop on shutdown

script

    echo $$ > /var/run/kafka.pid
    exec /srv/kafka/bin/kafka-server-start.sh /srv/kafka/config/server.properties

end script

pre-start script
    echo "[`date`] Kafka starting" >> /var/log/kafka.log
end script

pre-stop script
    rm /var/run/kafka.pid
    echo "[`date`] Kafka stopping" >> /var/log/kafka.log
end script
UPSTART

init-checkconf /etc/init/kafka.conf
sudo service kafka start

echo "Kafka broker installed and started."
touch $INSTALLED

