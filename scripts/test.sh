#!/bin/bash
set -e
export DJANGO_SETTINGS_MODULE=simple_csv_api.settings

python -m pycodestyle --exclude=migrations --max-line-length=100 simple_csv_api/
python -m mypy simple_csv_api/ --exclude env/
python -m pytest --cov=api/ tests/*