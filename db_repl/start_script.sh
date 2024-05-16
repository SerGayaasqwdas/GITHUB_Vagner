#!/bin/bash

rm -rf /var/lib/postgresql/data/*
until pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --host=db_image --port=$PGPORT -U $USERNAME_BD_REPL <<EOF
$PASSWORD_REPL
EOF
do
sleep 2s
echo 'Waiting for primary to connect...'
sleep 1s
done
echo 'Backup done, starting replica...'

chmod 0700 /var/lib/postgresql/data
postgres
