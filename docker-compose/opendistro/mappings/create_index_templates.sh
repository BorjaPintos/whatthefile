#!/bin/bash

create_index_template() {
    curl -X PUT --insecure -u "$2" \
      "$1"/_index_template/analysis_index_template \
      -H 'Content-Type: application/json' \
      -H 'cache-control: no-cache' \
      -d @analysis_index_template.json

    curl -X PUT --insecure -u "$2" \
      "$1"/_index_template/evtx-index-template \
      -H 'Content-Type: application/json' \
      -H 'cache-control: no-cache' \
      -d @evtx_index_template.json
}

if [[ $# != 2 ]]
then
  echo "usage: sh $0 ELASTICSEARCH_URL" "user:password"
else
  create_index_template "$1" "$2"
fi