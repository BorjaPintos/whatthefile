#!/bin/sh
echo "waiting for tika ..."
while ! $(curl --output /dev/null --silent --head --fail http://tika:9998); do
    >&2 echo "waiting for tika..."
    sleep 1
done

pip3 install -r /whatthefile/application/web/requirementsweb.txt
python3 runserverpro.py

echo "Analysis Done!"
