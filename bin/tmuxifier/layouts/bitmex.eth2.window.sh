# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "eth2"

# Split window into panes.
split_v 50
#split_v 50 1

# Run commands.
run_cmd ". /mldev/bin/virtualenv/vdir000_2.7.6/bin/activate" 0
run_cmd ". /mldev/bin/virtualenv/vdir000_2.7.6/bin/activate" 1

run_cmd "kernprof -l bitmex.py -r01 -eth 2   -model t1pi -n 50 | less -SRi" 0
#run_cmd "kernprof -l bitmex.py -r01 -eth all -model t1pi -n 50 | less -SRi" 1

# Paste text
send_keys "kernprof -l bitmex.py -r01 -eth  -model t1pi -n 50 | less -SRi" 1

# Set active pane.
select_pane 0

