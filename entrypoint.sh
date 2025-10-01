#!/bin/sh

# entrypoint.sh

# 1. Ukonči skript, pokud jakýkoliv příkaz selže
set -e

# 2. Počkej, dokud není databáze opravdu připravená
echo "Waiting for database to be ready..."
# Použijeme malý Python skript pro ověření, že se lze připojit na port databáze
# 'db' je název služby z docker-compose.yml
python -c "
import socket
import time
while True:
    try:
        with socket.create_connection(('db', 5432), timeout=5):
            break
    except OSError:
        time.sleep(1)
"
echo "Database is ready."

# 3. Spusť databázové migrace
echo "Running database migrations..."
alembic upgrade head
echo "Migrations finished."

# 4. Spusť hlavní příkaz (FastAPI server), který byl předán z docker-compose
exec "$@"