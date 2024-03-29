#!/bin/sh
echo "waiting for tika ..."
while ! $(curl --output /dev/null --silent --head --fail http://tika:9998); do
    >&2 echo "waiting for tika..."
    sleep 1
done
while ! $(curl --insecure --output /dev/null --silent --head --fail -u admin:admin https://opensearch:9200); do
    >&2 echo "waiting for opensearch..."
    sleep 1
done

python3 whatthefile.py whatthefile.ini /input

echo "Analysis Done!"
