# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
#window_root "/ml.dev/lib/oanda/oandapy"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "ipn[ipy]"

# Split window into panes.
#split_v 33 0
split_v 50 0
#split_h 50

# Run commands.
run_cmd "p" 0
run_cmd "p" 1
run_cmd "cd /ml.dev/bin/" 0
#run_cmd "cd /sec/assets" 1
run_cmd "ipn" 0
#run_cmd "ipn" 1

# Paste text

# Set active pane.
#select_pane 0
