#!/bin/bash

INSTALLED=".crate.installed"

if [ -f "$INSTALLED" ]; then
	echo "Crate DB already installed"
	exit
fi

echo "Installing CrateDB ..."

sudo apt-get -y install python-software-properties
sudo apt-get -y install software-properties-common

sudo add-apt-repository -y ppa:crate/stable
sudo apt-get -y update
sudo apt-get -y install crate

touch ~/${INSTALLED}

sudo service crate restart

