#!/bin/bash

cp /backups/backups_virtualhost.conf /etc/nginx/sites-enabled/
/etc/init.d/nginx reload

python3 /backups/yandex/ya_disk_backup.py

rm /etc/nginx/sites-enabled/backups_virtualhost.conf
/etc/init.d/nginx reload
