#!/bin/bash


INSTALLED=".cassandra-lucene-index.installed"

if [ -f "$INSTALLED" ]; then
	echo "Cassandra already installed"
	exit
fi

echo "Installing Cassandra Lucene Index ..."

sudo apt-get -y install git maven
git clone http://github.com/Stratio/cassandra-lucene-index
cd cassandra-lucene-index
git checkout 3.9.0
mvn clean package
sudo cp plugin/target/cassandra-lucene-index-plugin-*.jar /usr/share/cassandra/

sudo pkill -f CassandraDaemon

sudo service cassandra restart

touch ~/${INSTALLED}


