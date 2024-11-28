#!/bin/bash

script_dir="$(dirname "$0")"
ps aux | awk '{print $1 ";" $2 ";" $3 ";" $4 ";" $5 ";" $6 ";" $7 ";" $11}' > "$script_dir/db.csv"