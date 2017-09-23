#!/bin/bash

fname="/mldev/bin/data/cache/coins/etherdelta.volume"
cp -p $fname.tsv $fname.2.tsv
echo '' > $fname.tsv
nano $fname.tsv

