#!/bin/bash
systemctl start redis.service
start service mongod start

pip install -r requirements.txt

cd news_pipeline # &: run on background
python news_monitor.py &
python news_fetcher.py &
python news_deduper.py &

echo "=================================================="
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
