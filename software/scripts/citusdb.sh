#!/bin/bash

INSTALLED=".citusdb.installed"

if [ -f "$INSTALLED" ]; then
	echo "Citus DB already installed"
	exit
fi

echo "Installing Citus DB ..."

sudo apt-get update

curl https://install.citusdata.com/community/deb.sh | sudo bash

sudo apt-get -y install postgresql-9.6-citus-6.2

touch ~/${INSTALLED}


