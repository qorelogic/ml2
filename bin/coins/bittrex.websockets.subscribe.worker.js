/*
// producer.js
var zmq = require('zeromq')
  , sock = zmq.socket('push');

sock.bindSync('tcp://127.0.0.1:3000');
console.log('Producer bound to port 3000');

setInterval(function(){
  console.log('sending work');
  sock.send('some work');
}, 500);
*/
// worker.js
var zmq = require('zeromq')
//  , sock = zmq.socket('pull');
  , sock = zmq.socket('sub');
sock.subscribe('');

sock.connect('tcp://127.0.0.1:3000');
console.log('Worker connected to port 3000');

//sock.on('message', function(msg){
sock.on('message', function(msg){
  console.log('work: %s', msg.toString());
});
