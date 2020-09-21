#!/bin/bash

function exec_clickhouse_query() {
  SQL=$1
  echo -e "\n Executing ClickHouse query\n"
  echo "${SQL}"
  docker exec -it clickhouse bash -c "echo \"$SQL\" | clickhouse-client --multiline"
  echo "-----------------------------------------"
}

exec_clickhouse_query "$(cat ./sql/shadow_stream.sql)"
exec_clickhouse_query "$(cat ./sql/shadow_consumer.sql)"
exec_clickhouse_query "$(cat ./sql/shadow.sql)"
