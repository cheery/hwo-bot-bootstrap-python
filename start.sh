#!/bin/sh
source /usr/local/bin/virtualenvwrapper.sh
workon pingpongbot
python pingpongbot.py "$@" > game.log 2>&1 &
echo $! >> .pids
