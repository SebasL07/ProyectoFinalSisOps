#!/bin/bash

ps aux | awk '{print $1 ";" $2 ";" $3 ";" $4 ";" $5 ";" $6 ";" $7 ";" $11}' > db.csv