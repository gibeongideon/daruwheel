#!/usr/bin/env bash
celery -A spinpesa beat -l DEBUG
#celery -A spinpesa beat -l INFO
