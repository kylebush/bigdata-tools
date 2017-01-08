#!/bin/bash


INSTALLED=".cassandra-lucene-index.installed"

if [ -f "$INSTALLED" ]; then
	echo "Cassandra already installed"
	exit
fi

echo "Installing Cassandra Lucene Index ..."

sudo apt-get install git maven -y
git clone http://github.com/Stratio/cassandra-lucene-index
cd cassandra-lucene-index
git checkout 3.9.0
mvn clean package
cp plugin/target/cassandra-lucene-index-plugin-*.jar /usr/share/cassandra/
touch $INSTALLED

sudo service cassandra restart


