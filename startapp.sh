#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:5000 app:app --log-level debug

# export FLASK_ENV=development && python main.py --host 0.0.0.0 --port 5000


