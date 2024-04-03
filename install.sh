#!bin/bash

apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    --no-install-recommends \
    apt-utils

apt-get install -y \
    build-essential \
    pkg-config \
    default-jre \
    git

git clone https://github.com/samiemostafavi/gabriel-lego-server.git

wget -c http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh

conda create -y -n py27 python=2.7
source activate py27
conda install opencv=2.4
pip install --upgrade pip==9

cd gabriel-lego-server
pip install -r requirements.txt
python setup.py install

# Run control
python /root/miniconda2/envs/py27/bin/gabriel-control -l -d -n net1

# Run ucom
python /root/miniconda2/envs/py27/bin/gabriel-ucomm -s localhost:8021

# Run lego server
cd ~/gabriel-lego-server/gabriel-lego/
python proxy.py -s 127.0.0.1:8021
