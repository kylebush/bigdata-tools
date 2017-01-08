#!/usr/bin/env bash

INSTALLED=".java-8.installed"

if [ -f "$INSTALLED" ]; then
	echo "Java 8 already installed"
	exit
fi

echo "Installing Java 8 ..."

sudo apt-get -y install software-properties-common
sudo add-apt-repository -y ppa:webupd8team/java
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get -y install oracle-java8-installer

touch ~/${INSTALLED}



