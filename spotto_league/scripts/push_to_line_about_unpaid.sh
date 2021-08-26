#!/bin/bash
export PATH="$HOME/.poetry/bin:$PATH"
cd $(dirname $0)
poetry run python -m ponno_line.ponno_bot --method_name push_about_unpaid
