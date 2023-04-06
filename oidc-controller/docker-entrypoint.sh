#!/bin/bash
python3 -m alembic upgrade head
if [ $? == 0 ]; then
    exec uvicorn api.main:app --host 0.0.0.0 --port 5000 --log-level error --forwarded-allow-ips="*"
fi
echo 'Alembic db upgrade failed...'
exit 1
