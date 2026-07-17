#!/usr/bin/env bash
cd "$(dirname "$(readlink -f "$0")")" || exit 1
exec python3 link_viewer.py "$@" >> "$PWD/saver_launch.log" 2>&1
