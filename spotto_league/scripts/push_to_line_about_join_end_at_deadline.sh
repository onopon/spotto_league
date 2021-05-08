#!/bin/bash
# cd ~/web/spotto_league
cd $(dirname $0)
poetry run python -m ponno_linebot.ponno_bot --method_name push_about_join_end_at_deadline
