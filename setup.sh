#!/bin/bash

docker pull postgres:latest

if ! command -v astro &> /dev/null
then
    echo "Astro CLI could not be found, installing..."
    curl -sSl https://install.astronomer.io | sudo bash
fi

# astro start the database on it's own
astro dev start

MAX_ATTEMPTS=5
ATTEMPTS=0
POSTGRES_UP=false

while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    POSTGRES_CONTAINER=$(docker ps --filter "ancestor=postgres:12.6" --format "{{.Names}}" | head -n 1)
    if [ -n "$POSTGRES_CONTAINER" ] && docker exec $POSTGRES_CONTAINER pg_isready -U postgres; then
        POSTGRES_UP=true
        break
    else
        echo "Waiting for Postgres container to run..."
        sleep 30
        ATTEMPTS=$((ATTEMPTS+1))
    fi
done

if [ "$POSTGRES_UP" = false ]; then
    echo "Postgres container did not start within expected time. Exiting."
    astro dev stop
    exit 1
fi

DB_NAME="turbobank"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_SCHEMA="public"
SCHEMA_FILE="bank/schema.sql"

ACCOUNTS=150

VIRTUAL_ENV_DIR=".venv"


if docker exec $POSTGRES_CONTAINER psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
    echo "Database $DB_NAME already exists. Skipping creation."
else
    echo "Database $DB_NAME does not exist. Creating database, user, role, and schema..."
    docker exec -i $POSTGRES_CONTAINER psql -U postgres <<-EOSQL
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
        CREATE DATABASE $DB_NAME;
        GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
        \c $DB_NAME
        CREATE SCHEMA $DB_SCHEMA AUTHORIZATION $DB_USER;
EOSQL

    if [ -f "$SCHEMA_FILE" ]; then
        echo "Applying schema from $SCHEMA_FILE..."
        docker exec -i $POSTGRES_CONTAINER psql -U $DB_USER -d $DB_NAME < $SCHEMA_FILE
    else
        echo "Schema file $SCHEMA_FILE does not exist. Skipping schema application."
    fi
fi

echo "Database setup complete."

EXISTING_ACCOUNTS=$(docker exec $POSTGRES_CONTAINER psql -U postgres -d $DB_NAME -tAc "SELECT COUNT(id) FROM accounts;")
if [ "$EXISTING_ACCOUNTS" -eq 0 ]; then
    echo "No Accounts found."
    echo "Setting up Python environment and creating $ACCOUNTS..."

    if [ ! -d "$VIRTUAL_ENV_DIR" ]
    then
        python3 -m venv $VIRTUAL_ENV_DIR
    fi

    echo "Creating $ACCOUNTS accounts"
    export POSTGRES_CONN_ID="postgres://$DB_USER:$DB_PASSWORD@127.0.0.1:5432/$DB_NAME"

    source $VIRTUAL_ENV_DIR/bin/activate
    pip install -r requirements.txt

    python3 main.py create-accounts --accounts $ACCOUNTS
    echo "$ACCOUNTS accounts created"

    deactivate
else
    echo "There are already some accounts ($EXISTING_ACCOUNTS) exist. Skipping account creation."
fi