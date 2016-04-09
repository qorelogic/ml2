
// source: https://github.com/chjj/tty.js
var tty = require('tty.js');

var app = tty.createServer({
  shell: 'bash',
  users: {
    //qore: '728e1e6e353c4c9ca6275ebfc9ab5088f7f99c99',
    //qore: 'demo',
    //demo: 'demo'
    foo: 'bar'
  },
  port: 8000
});

app.get('/foo', function(req, res, next) {
  res.send('bar');
});

app.listen();
