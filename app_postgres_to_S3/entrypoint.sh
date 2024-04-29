#!/bin/bash
/bin/bash -c printenv > /etc/environment

# Start cron in the background
service cron start

# Add cron job
(crontab -l ; echo "*/1 * * * * /usr/local/bin/python /app/app.py >> /var/log/cron.log 2>&1") | crontab -

# Tail the cron log to keep the container running
tail -f /var/log/cron.log

