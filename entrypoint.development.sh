#!/bin/sh
set -e

if [ ! -d "migrations" ]; then
  echo "Migrations folder not found. Initializing..."
  flask db init
fi

if [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
  echo "No migrations found. Creating initial migration..."
  flask db migrate -m "init"
fi

echo "Running database migrations..."
flask db upgrade

echo "Compiling SCSS..."
(cd src/static/ts && npx sass ../scss/main.scss:../css/main.css --style=compressed --no-source-map)

echo "Starting TypeScript + SCSS watcher..."
(cd src/static/ts && node scripts/watch-all.js) &

exec python app.py