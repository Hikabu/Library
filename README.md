# Library
nohup python /path/to/script.py >/dev/null 2>&1 &

pkill -f "python /path/to/script.py"

cat ~/.deletion_log.txt