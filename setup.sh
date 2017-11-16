#!/bin/sh

sudo apt-get install -y wget
sudo apt-get install -y python-pip

pip install azure


wget https://github.com/j-l-m/testrepo/raw/master/rec_msgs.py

nohup python rec_msgs.py &
nohup python rec_msgs.py &

