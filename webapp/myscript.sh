#!/bin/bash

set -e

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting script" >> /tmp/myscript.log
cd ../code/

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting page download" >> /tmp/myscript.log
python3 dlpage.py

echo "$(date '+%Y-%m-%d %H:%M:%S') Storing new data into db" >> /tmp/myscript.log
python3 storenewdata.py

echo "$(date '+%Y-%m-%d %H:%M:%S') Generate pontok.txt" >> /tmp/myscript.log
python3 generatepontok.py

echo "$(date '+%Y-%m-%d %H:%M:%S') Committing" >> /tmp/myscript.log
git add ../pontok.txt result.sqlite
git commit -m "$(date '+%Y-%m-%d %H:%M:%S')"

echo "$(date '+%Y-%m-%d %H:%M:%S') Pushing" >> /tmp/myscript.log
GIT_SSH_COMMAND='ssh -i /home/sasa/certs/githubkey' git push git@github.com:tothsandorcd/tippeldmeg.git

echo "$(date '+%Y-%m-%d %H:%M:%S') Execution finished" >> /tmp/myscript.log
