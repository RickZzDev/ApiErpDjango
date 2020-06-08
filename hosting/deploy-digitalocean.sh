#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo $DIR

tar cajf /tmp/folha.tar.bz2 \
        --exclude='*.pyc' \
        --exclude='*.sqlite3' \
        --exclude='local_settings.py' \
        --exclude='__pycache__' \
        --exclude='./external' \
        --exclude='./env' \
        --exclude='./.git' \
        -C $DIR/../ .

scp /tmp/folha.tar.bz2 tmpfolha:/tmp/

REMOTE_SCRIPT="rm -rf /home/folha/folha/;
mkdir /home/folha/folha/;
tar xajf /tmp/folha.tar.bz2 -C /home/folha/folha/;
export FOLHA_STATIC_ROOT=/home/folha/folha_files/static;
export FOLHA_MEDIA_ROOT=/home/folha/folha_files/media;
export FOLHA_TESTE=True;
cd /home/folha/folha/;
virtualenv --system-site-packages env;
source env/bin/activate;
pip install -r requirements.txt;
./manage.py migrate;
./manage.py collectstatic --noinput;
"
ssh tmpfolha $REMOTE_SCRIPT

ROOT_REMOTE_SCRIPT="
systemctl restart folha-gunicorn;
"
ssh tmpfolha-root $ROOT_REMOTE_SCRIPT
