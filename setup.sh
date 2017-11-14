#!/bin/sh
sudo apt install -y python-pip

pip install azure


wget https://github.com/j-l-m/testrepo/raw/master/cloud_7.py

python cloud_7.py

