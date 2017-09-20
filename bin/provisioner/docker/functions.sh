#!/bin/bash

dockerBuild() {
  sudo docker build -t feed.01 feed/
}

dockerRun() {
  sudo docker run -it --rm --name feed.01.01 feed.01
}

#dockerBuild
#dockerRun
