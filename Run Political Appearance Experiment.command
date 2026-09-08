#!/bin/zsh

set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"

if [[ ! -x ".venv/bin/python" ]]; then
    echo "Preparing the local experiment for first use..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Checking the experiment's Python packages..."
python -m pip install --quiet --disable-pip-version-check -r requirements.txt

export OTREE_ADMIN_PASSWORD="${OTREE_ADMIN_PASSWORD:-local-demo-admin}"
export OTREE_SECRET_KEY="${OTREE_SECRET_KEY:-appearance-poc-local-development}"

if [[ -f "db.sqlite3" ]]; then
    INSTALLED_SCHEMA_VERSION="$(python -c 'from otree.database import version_for_pragma; print(version_for_pragma())')"
    DATABASE_SCHEMA_VERSION="$(python - <<'PY'
import sqlite3

connection = sqlite3.connect('db.sqlite3')
print(connection.execute('PRAGMA user_version').fetchone()[0])
connection.close()
PY
)"

    if [[ "$DATABASE_SCHEMA_VERSION" != "$INSTALLED_SCHEMA_VERSION" ]]; then
        mkdir -p local_db_backups
        BACKUP_PATH="local_db_backups/db.sqlite3.$(date +%Y%m%d-%H%M%S).backup"
        mv db.sqlite3 "$BACKUP_PATH"
        echo "The older local database was preserved at $BACKUP_PATH."
    fi
fi

STUDY_URL="http://127.0.0.1:8000/demo/finland_appearance_poc"

(
    for attempt in {1..60}; do
        if curl --silent --fail --output /dev/null "http://127.0.0.1:8000/"; then
            open "$STUDY_URL"
            exit 0
        fi
        sleep 1
    done
    echo "The server did not become ready within one minute. Check this window for an error message."
) &

echo "Starting the English proof-of-concept experiment..."
echo "Keep this window open while using the study. Press Control-C to stop it."
echo "Study address: $STUDY_URL"
echo

exec otree devserver 8000
