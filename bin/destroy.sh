#!/bin/bash

sudo umount /mnt/*/*
df -h 

sudo wipe -fqQ10 datafeeds/config.csv
sudo wipe -rfqQ10 data/oanda/logs/
sudo wipe -rfqQ10 /root/.bash_history
sudo wipe -rfqQ10 /hoome/qore/.bash_history
sudo wipe -rfqQ10 *.ipynb
sudo wipe -rfqQ10 */*.ipynb
sudo wipe -rfqQ10 */*.py
