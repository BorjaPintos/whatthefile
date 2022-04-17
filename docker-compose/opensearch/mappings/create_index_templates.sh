#!/bin/bash

send_index_template() {
    echo "Sending template $4"
    curl -X PUT --insecure -u "$2" "$1"/_index_template/$3 -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d @$4
}


if [[ $# != 3 ]]
then
  echo "usage: sh $0 OPENSEARCH_URL USER:PASSWORD TEMPLATES_PATH"
  exit 0
fi

TEMPLATES_PATH=$3
TEMPLATES=$(ls $TEMPLATES_PATH)
for TEMPLATE in $TEMPLATES
do
   NAME_TEMPLATE=$(echo $TEMPLATE | cut -d "." -f 1)
   send_index_template "$1" "$2" $NAME_TEMPLATE $TEMPLATES_PATH/$TEMPLATE
done

