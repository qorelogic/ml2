

const bittrex = require('/mldev/lib/crypto/bittrex/n0mad01_node.bittrex.api.github.py.git/node.bittrex.api');
// producer.js
var zmq = require('zeromq')
//  , sock = zmq.socket('push');
  , sock = zmq.socket('pub');

sock.bindSync('tcp://127.0.0.1:3000');
console.log('Producer bound to port 3000');

var i = 1;

bittrex.options({ 
  'verbose' : true, 
});

//pairs = ['BTC-ETH','BTC-SC','BTC-ZEN']
pairs = ['BTC-ETH']
const websocketsclient = bittrex.websockets.subscribe(pairs, function(data) {
  if (data.M === 'updateExchangeState') {
    data.A.forEach(function(data_for) {
      console.log('Market Update for '+ data_for.MarketName, data_for);
      //console.log(data_for);
      var tjson = JSON.stringify(data_for)
      //console.log(typeof(data_for));
      //console.log(typeof(tjson));
      //console.log('sending work');
      //sock.send('some work '+i);

      //sock.send(data_for);
      sock.send(tjson);

      i++;
    });
  }
});


setInterval(function(){
/*
  console.log('sending work');
  sock.send('some work '+i);
  i++;
*/
}, 10);
