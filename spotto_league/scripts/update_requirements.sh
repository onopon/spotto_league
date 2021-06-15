#! /bin/sh
poetry export -f requirements.txt --output requirements.txt
poetry export --dev -f requirements.txt --output requirements_dev.txt
