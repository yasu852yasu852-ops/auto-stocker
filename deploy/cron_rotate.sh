#!/bin/bash
# Run monthly via cron (e.g. 0 0 1 * * /opt/auto-stocker/deploy/cron_rotate.sh)
/opt/auto-stocker/.venv/bin/python /opt/auto-stocker/services/log_rotator.py
