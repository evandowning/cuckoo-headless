#!/bin/bash

uid=`id -u`

# Check user permissions
if [[ $uid -ne 0 ]]; then
    echo 'must be root'
    exit 2
fi

# Stop on any error
set -e

# Update
apt update

# Requirements for parsing raw files
apt install -y python2.7
apt install -y python-pip
apt install -y python-bson
pip install -r requirements.txt
