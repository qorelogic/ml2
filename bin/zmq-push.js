
// producer.js
var zmq = require('zmq')
  , sock = zmq.socket('push');

porrt = 5555
sock.bindSync('tcp://127.0.0.1:'+porrt);
console.log('Producer bound to port '+porrt);
c = 0
setInterval(function(){
  //console.log('sending work');
  sock.send('some work '+c);
  c++;
}, 100);
