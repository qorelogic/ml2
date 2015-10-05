# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "mongod"

# Split window into panes.
split_v 50
#split_h 50 0

# Run commands.
run_cmd "sudo mongod --config=/etc/mongodb.conf" 0
run_cmd "tail -f /var/log/mongodb/mongodb.log" 1

# Paste text

# Set active pane.
select_pane 0
