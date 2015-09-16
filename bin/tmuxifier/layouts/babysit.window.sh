# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin/datafeeds"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "Babysitter"

# Split window into panes.
split_h 50
split_v 50 1

# Run commands.
run_cmd ".gpull" 0
run_cmd "python oanda.py babysit" 0
run_cmd ".gpull" 1
run_cmd "htop" 2

#send_keys "./push.sh" 1

# Set active pane.
select_pane 0
