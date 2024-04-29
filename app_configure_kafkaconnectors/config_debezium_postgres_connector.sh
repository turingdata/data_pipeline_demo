#!/bin/bash


curl -i -X POST -H "Accept:application/json" \
-H "Content-Type:application/json" \
"http://debezium:8083/connectors/" \
--data-raw '{
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "plugin.name": "pgoutput",
        "database.hostname": "postgres_for_webapp",
        "database.port": "5432",
        "database.dbname": "postgres",
        "database.user": "admin",
        "database.password": "password",
        "database.server.name": "postgres-webapp",
        "table.include.list": "public.trips",
        "topic.prefix": "webapp"
    },
    "name": "webapp_postgres"
}'