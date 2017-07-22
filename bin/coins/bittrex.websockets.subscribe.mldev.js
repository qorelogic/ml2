
const bittrex = require('/mldev/lib/crypto/bittrex/n0mad01_node.bittrex.api.github.py.git/node.bittrex.api');

bittrex.options({ 
  'verbose' : true, 
});

const websocketsclient = bittrex.websockets.subscribe(['BTC-ETH','BTC-SC','BTC-ZEN'], function(data) {
  if (data.M === 'updateExchangeState') {
    data.A.forEach(function(data_for) {
      console.log('Market Update for '+ data_for.MarketName, data_for);
    });
  }
});

/*
// producer.js
var zmq = require('zeromq')
  , sock = zmq.socket('push');

sock.bindSync('tcp://127.0.0.1:3000');
console.log('Producer bound to port 3000');

var i = 1;

setInterval(function(){
  console.log('sending work');
  sock.send('some work '+i);
  i++;
}, 10);
*/