# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.live/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "ml.live"

# Split window into panes.
split_v 50
#split_h 50

# Run commands.
#run_cmd "top"     # runs in active pane
#run_cmd "date" 1  # runs in pane 1
run_cmd "cd /ml.live/bin" 0
run_cmd "cd /ml.live/bin" 1
run_cmd "p" 0
run_cmd "p" 1
run_cmd "ls && git branch -v" 1

# Paste text
#send_keys "top"    # paste into active pane
#send_keys "date" 1 # paste into pane 1

# Set active pane.
#select_pane 0
