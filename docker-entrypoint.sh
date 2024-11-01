#!/bin/sh
set -e

# Wait for the database to be ready
until python -m todo.manage migrate
do
  echo "Waiting for database to be ready..."
  sleep 2
done

# Collect static files
python -m todo.manage collectstatic --noinput

# Start the server
exec "$@"
