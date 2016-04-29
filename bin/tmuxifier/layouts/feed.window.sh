# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "feed"

# Split window into panes.
split_v 50
split_v 50 0
split_h 50 1
split_h 50 0

# Run commands.
run_cmd "cd datafeeds/" 0
run_cmd "kernprof -lv oanda.py feed" 0
run_cmd ". /mldev/bin/functions.sh; _mongod" 1
#run_cmd "tail -f /var/log/mongodb/mongod.log" 1
run_cmd "watch -n3 \"mongo --quiet --eval 'db.ticks.stats()[\\\"count\\\"]' ql\"" 2
run_cmd ". /mldev/bin/functions.sh; _mongodlog" 3
run_cmd "kernprof -lv simulator.py -n 4000 -v" 4

# Paste text

# Set active pane.
select_pane 1
