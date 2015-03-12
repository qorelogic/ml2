# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
#window_root "~/Projects/procsys"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "procsys"

# Split window into panes.
split_h 50
split_v 50 0
split_v 50 1
split_v 50 2
split_v 50 3
#split_h 50

# Run commands.
run_cmd "htop" 0
run_cmd "watch -n1 'ls -lt /var/log/*log | head'" 1
run_cmd "sudo iotop" 2
run_cmd "watch -n5 'acpi -V'" 3
run_cmd "sudo hddtemp /dev/sda" 4
run_cmd "watch -n60 'du -sc /ml.dev/bin/data/oanda/datafeed/'" 5

# Paste text
#send_keys "top"    # paste into active pane
#send_keys "date" 1 # paste into pane 1

# Set active pane.
select_pane 1
