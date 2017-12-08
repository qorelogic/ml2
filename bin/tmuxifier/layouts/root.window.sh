# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/mldev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "root"

## Split window into panes.
#split_v 66
#split_v 50 1

## Run commands.
##run_cmd ".gpull" 0
#run_cmd "python main.py" 0
#run_cmd "nano /mldev/bin/data/1broker/balances.json" 1
#run_cmd "python main.py" 2

#send_keys "l" 2

#===

# Split window into panes.
split_v 50
#split_h 50 1

# Run commands.
run_cmd "sudo su" 0
run_cmd "sudo su" 1

#send_keys "python zmq-client.py 127.0.0.1:5555 avg" 0


# Set active pane.
select_pane 0
