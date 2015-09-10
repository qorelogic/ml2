
# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/mldev/lib/crawlers/finance/dataPipeline.scrapy/"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "DataMiner"

# Split window into panes.
split_h 50

# Run commands.
run_cmd "tail -f /mldev/bin/data/infofeeds/logs/dataminer.log" 0
run_cmd "tail -f /mldev/bin/data/infofeeds/logs/dataminer.err.log" 1

# Set active pane.
select_pane 0
