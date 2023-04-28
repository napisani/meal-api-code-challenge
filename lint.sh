#!/usr/bin/env bash
ruff check ayble_health_api --fix
mypy ayble_health_api
