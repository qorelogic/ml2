# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "/ml.dev/bin"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "solidity"

# Split window into panes.
split_v 70
#split_h 50 0
split_h 50 1
split_v 50 0

# Run commands.
run_cmd "cd /mldev/lib/crypto/ethereum/ethereum_browser-solidity.github.py.git/" 0
run_cmd "npm start" 0
run_cmd "/usr/local/bin/remixd -S solidity/" 3

#run_cmd 'geth --networkid 42 --nodiscover --rpc --rpccorsdomain "*" console' 1
#run_cmd "web3" 1

#run_cmd 'node' 1
#run_cmd "Web3 = require('web3');" 1
#run_cmd 'var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));' 1
#run_cmd "web3" 1

run_cmd "sleep 3" 2
run_cmd 'node' 2
run_cmd "Web3 = require('web3');" 2
run_cmd 'var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));' 2
run_cmd "web3.eth.accounts" 2

run_cmd "testrpc" 1

#run_cmd "" 1

# Paste text
#send_keys """ 0

# Set active pane.
select_pane 2

