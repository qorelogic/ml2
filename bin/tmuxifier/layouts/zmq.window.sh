# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "zmq"

# Split window into panes.
split_h 50
split_v 50 0
split_v 50 1

# Run commands.
run_cmd ".gpull" 0
#run_cmd "python zmq-server.py" 0
run_cmd "cd datafeeds/" 0
run_cmd "./babysit.sh" 0
run_cmd " python zmq-client.ws.py" 2
run_cmd " python zmq-client.flask.py" 3
run_cmd "htop" 1

send_keys "./qlm.sh" 0
send_keys "./push.sh" 1

# Set active pane.
select_pane 0
