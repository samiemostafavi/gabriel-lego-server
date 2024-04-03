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
    screen \
    git

git clone https://github.com/samiemostafavi/gabriel-lego-server.git

wget -c http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh
source .bashrc

conda create -y -n py27 python=2.7
source activate py27
conda install opencv=2.4.9
pip install --upgrade pip==9

cd gabriel-lego-server
pip install -r requirements.txt
python setup.py install

# Now we create 3 screen sessions to run 3 python apps at the same time:

# control app
# create and enter a new session named control by
screen -S control
# run control app by
source activate py27
python /root/miniconda2/envs/py27/bin/gabriel-control -l -d -n net1
# then detach from this screen session by:
# press 'ctrl' and 'a' at the same time, and then press 'd'

# ucom app
# create and enter a new session named ucom by
screen -S ucom
source activate py27
# run ucom app by
python /root/miniconda2/envs/py27/bin/gabriel-ucomm -s localhost:8021
# then detach from this screen session by:
# first, press 'ctrl' and 'a' at the same time, and then press 'd' to detach from the session

# lego-server app
# create and enter a new session named lego by
screen -S lego
# run lego-server app by
source activate py27
cd ~/gabriel-lego-server/gabriel-lego/
python proxy.py -s 127.0.0.1:8021
# then detach from this screen session by:
# first, press 'ctrl' and 'a' at the same time, and then press 'd' to detach from the session

# you can re-enter the screen sessions to check the logs by
# screen -r control
# screen -r ucom
# screen -r lego

# you can kill the sessions by first entering them and then
# first, press 'ctrl' and 'a' at the same time, and then press 'k' to kill the session
