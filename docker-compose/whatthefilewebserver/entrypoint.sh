#!/bin/sh
echo "waiting for tika ..."
while ! $(curl --output /dev/null --silent --head --fail http://tika:9998); do
    >&2 echo "waiting for tika..."
    sleep 1
done

python3.7 runserverpro.py

echo "Analysis Done!"
