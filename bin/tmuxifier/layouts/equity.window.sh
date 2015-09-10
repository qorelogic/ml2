# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin/data/oanda/logs"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "equity(oanda)"

# Split window into panes.
split_v 60
split_v 50 1
split_h 50 1

# Run commands.
qrun_cmd() {
run_cmd "p" $2
run_cmd "tail -f $1.equity.log.csv" $2
}

qrun_cmd kpql 1
qrun_cmd sublimation 3
qrun_cmd kpqldemo 2

run_cmd "watch -n2 'ls -lt /ml.dev/bin/data/oanda/logs'" 0

# Set active pane.
select_pane 0
