#!/bin/bash
/bin/bash -c printenv > /etc/environment

# Start cron in the background
service cron start

cd datawarehouse

dbt deps

dbt build


# Add cron job
(crontab -l ; echo "*/10 * * * * cd /dbt/datawarehouse ; /usr/local/bin/dbt run  >> /var/log/cron.log 2>&1") | crontab -

# Tail the cron log to keep the container running
tail -f /var/log/cron.log

