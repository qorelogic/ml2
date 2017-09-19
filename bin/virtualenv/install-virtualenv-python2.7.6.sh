#!/bin/bash

# source: https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4
# source: http://docs.python-guide.org/en/latest/dev/virtualenvs/
# source: http://stackoverflow.com/questions/32054580/httpshandler-error-while-installing-pip-with-python-2-7-9

vinstall() {
# https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4
wget -nc http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
tar -Jxf Python-2.7.6.tar.xz

sudo apt-get install virtualenv
#http://stackoverflow.com/questions/32054580/httpshandler-error-while-installing-pip-with-python-2-7-9
sudo apt-get install libssl-dev
sudo apt-get install zlib1g-dev

py276="/mldev/bin/virtualenv/opt/python-2.7.6"
mkdir -p $py276

cd Python-2.7.6
./configure --with-zlib --prefix=$py276
make clean
make
make altinstall
cd ../

virtualenv -p $py276/bin/python2.7 vdir000_2.7.6
}

installMlDev() {
. ./vdir000_2.7.6/bin/activate
if [ "`python -V 2>&1`" == "Python 2.7.6" ]; then
# http://stackoverflow.com/questions/17892071/pip-install-error-setuptools-command-not-found
pip install -U setuptools

# turn swap on
# http://stackoverflow.com/questions/18334366/out-of-memory-issue-in-installing-packages-on-ubuntu-server
sudo dd if=/dev/zero of=/tmp/swapfile1 bs=1024 count=524288
sudo mkswap /tmp/swapfile1
sudo chown root:root /tmp/swapfile1
sudo chmod 0600 /tmp/swapfile1
sudo swapon /tmp/swapfile1

# https://github.com/kivy/buildozer/issues/150
pip install Cython==0.23

pip install numpy
pip install pandas

pip install ujson
pip install pyzmq
pip install pymongo
pip install celery
pip install flask
pip install html2text
pip install plotly
sudo apt-get install libfreetype6-dev libxft-dev
pip install matplotlib
pip install TA-lib

# swapp off
sudo swapoff -v /tmp/swapfile1
sudo rm -f /tmp/swapfile1

pip freeze

else

echo 'python not 2.7.6'

fi
}

vinstall
installMlDev
