#!/bin/bash
echo "Initializing database..."
python init_db.py
echo "Starting bot..."
python bot.py
