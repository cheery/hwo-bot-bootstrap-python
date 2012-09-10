#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
env_name=pingpongbot
if [ ! -d ~/.virtualenvs/$env_name ]; then
    mkvirtualenv $env_name
fi
workon $env_name
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi
