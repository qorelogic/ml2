# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
#window_root "~/Projects/rapidminer"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "rapidminer"

# Split window into panes.
split_v 50
#split_h 50

# Run commands.
run_cmd "p" 0
run_cmd "p" 1
run_cmd "cd /Opt/Downloads/rapidminer/" 0
run_cmd "cd /Opt/Downloads/rapidminer/" 1

# Paste text
send_keys "java -jar lib/rapidminer.jar" 1

# Set active pane.
#select_pane 0
