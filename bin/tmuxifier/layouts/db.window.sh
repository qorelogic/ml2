# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "db"

# Split window into panes.
split_v 66
split_v 50 1

# Run commands.
run_cmd "watch -n3 \"mongo --quiet --eval 'db.investingWorldGovernmentBonds.stats()[\\\"count\\\"]' numbeo\"" 0
run_cmd "watch -n3 \"mongo --quiet --eval 'db.equity.stats()[\\\"count\\\"]' ql\"" 1
run_cmd "watch -n3 \"mongo --quiet --eval 'db.ticks.stats()[\\\"count\\\"]' ql\"" 2

# Paste text
#send_keys "watch -n3 \"mongo --quiet --eval 'db.equity.stats()[\\\"count\\\"]' ql\"" 0

# Set active pane.
select_pane 0
