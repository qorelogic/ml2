
Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
//console.log(web3);

web3.eth.getBalance(web3.eth.accounts[1])

//from = web3.eth.getBalance(web3.eth.accounts[1]);

eth = {'to':web3.eth.accounts[1], 'from': web3.eth.accounts[0]};

//console.log(eth);

var send = web3.eth.sendTransaction({from:eth.from, to:eth.to, value:web3.toWei(0.05, "ether")});

console.log(web3.eth.getBalance(web3.eth.accounts[1])['c'][0]);
