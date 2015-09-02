#!/bin/bash

git add oanda/qorequant/*
git commit -m 'update theta train' .
#.gpull
git pull origin master
#.gpush
git push origin master
