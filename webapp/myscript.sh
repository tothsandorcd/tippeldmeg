#!/bin/bash

set -e

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting script" | tee /tmp/myscript.log
cd ../code/

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting page download" | tee /tmp/myscript.log
python3 dlpage.py

echo "$(date '+%Y-%m-%d %H:%M:%S') Storing new data into db" | tee /tmp/myscript.log
python3 storenewdata.py

echo "$(date '+%Y-%m-%d %H:%M:%S') Generate pontok.txt" | tee /tmp/myscript.log
python3 generatepontok.py

echo "$(date '+%Y-%m-%d %H:%M:%S') Committing" | tee /tmp/myscript.log
git add ../pontok.html result.sqlite
git commit -m "$(date '+%Y-%m-%d %H:%M:%S')"

echo "$(date '+%Y-%m-%d %H:%M:%S') Pushing" | tee /tmp/myscript.log
GIT_SSH_COMMAND='ssh -i /home/sasa/certs/githubkey' git push git@github.com:tothsandorcd/tippeldmeg.git

echo "$(date '+%Y-%m-%d %H:%M:%S') Execution finished" | tee /tmp/myscript.log
