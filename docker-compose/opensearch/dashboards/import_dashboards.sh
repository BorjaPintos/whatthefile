#!bin/bash

send_objects() {
    curl -XPOST --insecure -u $2 "$1"/api/saved_objects/_import?overwrite=true -H "osd-xsrf:true" --form file=@$3
}


if [[ $# != 3 ]]
then
  echo "usage: sh $0 OPENSEARCH_DASHBOARDS_URL USER:PASSWORD DASHBOARDS_PATH"
  exit 0
fi

DASHBOARDS_PATH=$3
DASHBOARDS=$(ls $DASHBOARDS_PATH)
for DASHBOARD in $DASHBOARDS
do
   send_objects "$1" "$2" $DASHBOARDS_PATH/$DASHBOARD
done
