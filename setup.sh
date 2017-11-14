#!/bin/sh

sudo apt-get install -y wget
sudo apt-get install -y python-pip

pip install azure


wget https://github.com/j-l-m/testrepo/raw/master/cloud_7.py

nohup python cloud_7.py &
nohup python cloud_7.py &

