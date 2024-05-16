#!/bin/bash

#mkdir -p /var/lib/postgresql/WAL/archive
mkdir -p /var/lib/postgressql/data/logs

psql -U "$POSTGRES_USER" -d $POSTGRES_DB -c \
"
CREATE USER $USERNAME_BD_REPL REPLICATION LOGIN ENCRYPTED PASSWORD '$PASSWORD_REPL';
SELECT * FROM pg_create_physical_replication_slot('replication_slot');

CREATE TABLE IF NOT EXISTS emails(
    user_id VARCHAR(50) PRIMARY KEY NOT NULL,
    found_emails VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS phones(
    user_id VARCHAR(50) PRIMARY KEY NOT NULL,
    found_numbers_phone VARCHAR(500)
);
"
