#!/bin/bash

echo "starting"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env


# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/container.env
*/5 * * * * /usr/bin/python3 /main.py >> /var/log/cron.log 2>&1
*/5 * * * * date >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
