# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "sparkling-water"

# Split window into panes.
split_v 50
split_h 50 1

# Run commands.
run_cmd ".gpull" 0
run_cmd "git branch" 0
run_cmd "cd /mldev/lib/ml/spark/sparkling-water-1.4.3/bin" 0
run_cmd "htop" 2

send_keys "./sparkling-shell" 0

# Set active pane.
select_pane 0
