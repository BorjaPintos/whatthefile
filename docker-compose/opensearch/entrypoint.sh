#/bin/bash

apt update && apt-get install -y curl
chmod +x /config/mappings/create_index_templates.sh
chmod +x /config/dashboards/import_dashboards.sh


while [[ "$(curl -s -o /dev/null -L  --insecure -u "$OPENSEARCH_AUTH" -H 'Content-Type: application/json' -H 'cache-control: no-cache' -w ''%{http_code}'' $OPENSEARCH_HOST)" != "200" ]];
    do 
        echo "Waiting for $OPENSEARCH_HOST" && sleep 2;
    done
/config/mappings/create_index_templates.sh $OPENSEARCH_HOST $OPENSEARCH_AUTH /config/mappings/templates


while [[ "$(curl -s -o /dev/null -L  --insecure -u "$OPENSEARCH_AUTH" -H 'Content-Type: application/json' -H 'cache-control: no-cache' -w ''%{http_code}'' $OPENSEARCH_DASHBOARDS_HOST)" != "200" ]];
    do 
        echo "Waiting for $OPENSEARCH_DASHBOARDS_HOST" && sleep 2;
    done
/config/dashboards/import_dashboards.sh $OPENSEARCH_DASHBOARDS_HOST $OPENSEARCH_AUTH /config/dashboards/objects
