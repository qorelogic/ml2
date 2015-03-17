# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin/data/oanda/datafeed"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "datafeeds"

# Split window into panes.
split_v 50
split_h 50 0
split_h 50 1
split_v 50 1
split_v 50 3

# Run commands.
qrun_cmd() {
run_cmd "p" $2
run_cmd "tail -f $1.csv" $2
}

qrun_cmd EUR_USD 0
qrun_cmd USD_JPY 1
qrun_cmd GBP_USD 2
qrun_cmd USD_CAD 3

send_keys "watch -n1 'ls -lt /ml.dev/bin/data/oanda/datafeed'" 4
#send_keys "cd /ml.dev/bin/datafeeds/ && celery worker -A mqtasks -l INFO" 5
send_keys "cd /ml.live/bin/datafeeds/ && python oanda.py" 5

# Paste text
#send_keys "top"    # paste into active pane
#send_keys "date" 1 # paste into pane 1

# Set active pane.
select_pane 4
