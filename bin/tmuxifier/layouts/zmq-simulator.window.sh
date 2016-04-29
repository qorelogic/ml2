# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/mldev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "zmq-simulator"

## Split window into panes.
#split_v 66
#split_v 50 1

## Run commands.

#send_keys "l" 2

#===

# Split window into panes.
split_v 50
#split_h 50 0

# Run commands.
#run_cmd "sudo su" 0
run_cmd "p && qp" 0
#run_cmd "python zmq-client.py :5555 avg" 0
#run_cmd "python zmq-client.py 104.207.135.67:5555 avg" 0
run_cmd "python zmq-client.py 127.0.0.1:5555 avg" 0
#run_cmd "python simulator.py" 1
run_cmd "python untitled.ui.py -nc 'EUR_USD,GBP_USD,USD_JPY,AUD_USD' -p 5557" 1

#send_keys "" 0

# Set active pane.
select_pane 0
