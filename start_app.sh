#!/bin/bash
echo "$@"

python3 check_db.py
alembic upgrade head
python3 app.py "$@"