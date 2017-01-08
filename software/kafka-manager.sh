#!/bin/bash

echo "Installing Kafka Manager ..."

ZK_HOST=$1
ZK_PORT=$2

INSTALLED=".kafka-manager.installed"

if [ -f "$INSTALLED" ]; then
	echo "Kafka already installed"
	exit
fi


sudo apt-get install unzip git -y

git clone https://github.com/yahoo/kafka-manager.git

cd kafka-manager
./sbt clean dist

cd target/universal
unzip kafka-manager*.zip
rm kafka-manager*.zip
sudo mv kafka-manager* /srv/kafka-manager

echo "Adding Kafka Manager upstart ..."

cat <<UPSTART >> /etc/init/kafka-manager.conf
description "Service for Kakfa Manager"
author      "Kyle Bush"

start on filesystem or runlevel [2345]
stop on shutdown

script

    echo $$ > /var/run/kafka-manager.pid
    exec /srv/kafka-manager/bin/kafka-manager -Dkafka-manager.zkhosts="${ZK_HOST}:${ZK_PORT}"

end script

pre-start script
    echo "[`date`] Kafka Manager starting" >> /var/log/kafka-manager.log
end script

pre-stop script
    rm /var/run/kafka-manager.pid
    echo "[`date`] Kafka Manager stopping" >> /var/log/kafka-manager.log
end script
UPSTART

init-checkconf /etc/init/kafka-manager.conf
sudo service kafka-manager start
echo "Kafka Manager installed and started."
touch $INSTALLED
