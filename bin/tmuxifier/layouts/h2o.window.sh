# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "h2o"

# Split window into panes.
split_v 50
split_h 50 1

# Run commands.
run_cmd ".gpull" 0
run_cmd "git branch" 0
#run_cmd "cd /mldev/lib/ml/h2o/h2o-2.8.4.4/" 0
run_cmd "cd /mldev/lib/ml/h2o/h2o-3.0.1.7/" 0
run_cmd "htop" 2

send_keys "java -jar h2o.jar" 0
#send_keys "./push.sh" 1

# Set active pane.
select_pane 0
