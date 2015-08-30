#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

if [ "`which vagrant`" == "" ]; then
	wget --no-check-certificate -c https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.4_i686.deb #-P tmp/
	sudo dpkg -i /tmp/vagrant_1.7.4_i686.deb
	rm -fv /tmp/vagrant_1.7.4_i686.deb
fi
if [ "`which virtualbox`" == "" ]; then
	sudo apt-get install virtualbox
fi

# source: https://atlas.hashicorp.com/ubuntu/boxes/trusty32
vagrant init ubuntu/trusty32 2> /dev/null
vagrant up --provider virtualbox
