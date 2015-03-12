# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/lib/oanda/oandapy"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "oandapy"

# Split window into panes.
split_v 50
#split_h 50

# Run commands.
run_cmd "p" 0
run_cmd "ipn" 0
run_cmd "p" 1

# Paste text
#send_keys "top"    # paste into active pane
#send_keys "date" 1 # paste into pane 1

# Set active pane.
#select_pane 0
