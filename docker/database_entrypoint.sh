#!/bin/sh
set -e

# Ensure data directory exists and has proper permissions
mkdir -p "${POSTGRES_DATA_DIR}"
chown -R postgres:postgres "${POSTGRES_DATA_DIR}"
chmod 700 "${POSTGRES_DATA_DIR}"

# Initialize database if empty
if [ ! -s "${POSTGRES_DATA_DIR}/PG_VERSION" ]; then
    echo "Initializing database..."
    initdb --username=postgres --pwfile=<(echo "$POSTGRES_PASSWORD") -D "${POSTGRES_DATA_DIR}"
fi

# Configure PostgreSQL to listen on all interfaces
echo "listen_addresses='*'" >> "${POSTGRES_DATA_DIR}/postgresql.conf"

# Set port from environment variable if provided
if [ -n "${POSTGRES_PORT}" ]; then
    echo "port = ${POSTGRES_PORT}" >> "${POSTGRES_DATA_DIR}/postgresql.conf"
fi

# Allow host connections (for development)
echo "host all all 0.0.0.0/0 md5" >> "${POSTGRES_DATA_DIR}/pg_hba.conf"

# Start PostgreSQL in background
postgres -D "${POSTGRES_DATA_DIR}" -c "config_file=${POSTGRES_DATA_DIR}/postgresql.conf" &

# Wait for server to start
sleep 5

# Create user if it doesn't exist
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${POSTGRES_USER}') THEN
       CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';
   END IF;
END
\$do\$;
EOSQL

# Create database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
SELECT 'CREATE DATABASE ${POSTGRES_DB}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname='${POSTGRES_DB}')\gexec
EOSQL

# Grant privileges on the database
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};
EOSQL

# Ensure schema ownership and privileges inside the app database
psql -v ON_ERROR_STOP=1 --username postgres --dbname=${POSTGRES_DB} <<-EOSQL
ALTER SCHEMA public OWNER TO ${POSTGRES_USER};
GRANT ALL PRIVILEGES ON SCHEMA public TO ${POSTGRES_USER};
EOSQL

# Keep PostgreSQL running in foreground
wait
