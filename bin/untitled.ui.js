/*
var program = require('blessed')();

program.alternateBuffer();  
program.enableMouse();  
program.hideCursor();

program.bg('red');

program.on('mouse', function(data) {  
  if (data.action === 'mousedown') {
    program.move(data.x, data.y);
    program.write(' ');
  }
});

program.on('keypress', function(ch, key) {  
  if (key.name === 'q') {
    program.disableMouse();
    program.showCursor();
    program.normalBuffer();
    process.exit(0);
  }
});

*/

var blessed = require('blessed');
var Client = require('node-rest-client').Client;
var client = new Client();

var http = require('http')
  , vm = require('vm')
  , concat = require('concat-stream'); // this is just a helper to receive the
                                       // http payload in a single callback
                                       // see https://www.npmjs.com/package/concat-stream

// source: http://stackoverflow.com/questions/7809397/how-to-require-from-url-in-node-js
// http://developer.oanda.com/oandajs/oanda.js
http.get({
    host: 'developer.oanda.com', 
    port: 80, 
    path: '/oandajs/oanda.js'
  }, 
  function(res) {
    res.setEncoding('utf8');
    res.pipe(concat({ encoding: 'string' }, function(remoteSrc) {
      vm.runInThisContext(remoteSrc, 'oandajs/oanda.js');
    }));
});

/*OANDA.rate.quote(['EUR_USD'], function(response) {
    if(response && !response.error) {
        var bid = response.prices[0].bid;
        var ask = response.prices[0].ask;
        // Do something with prices
        // ...
    }
});*/

/*
var oneBroker = require('1broker');
var oB = new oneBroker('62f188347a028f892a8570c9be41bc8e	');
    try {
    ai = oB.accountInfo();
    console.log(ai);
    } catch(err) {

    }
*/

// Create a screen object.
var screen = blessed.screen();

// Create a box perfectly centered horizontally and vertically.
var outer = blessed.box({  
  fg: 'blue',
  bg: 'default',
  border: {
    type: 'line',
    fg: '#ffffff'
  },
  tags: true,
  content: '{center}{red-fg}Liquidity Provider{/red-fg}{/center}\n'
         + '{right}world!{/right}',
  width: '75%',
  height: '50%',
  top: '10',
  left: '250'
});

// Append our box to the screen.
screen.append(outer);

// ---
var newTradeBuy = blessed.box({  
  parent: outer,
  top: '100',
  left: '10',
  width: '47.5%',
  height: '500',
  border: {
    type: '',
    fg: '#ffffff'
  },
  fg: 'white',
  bg: 'gray',
  content: '{bold}Buy{/bold}',
  tags: true,
  hoverEffects: {
    bg: '#aaaaaa'
  }
});
newTradeBuy.on('click', function(data) {  
    //newTradeBuy.setContent('{center}You clicked {red-fg}me{/red-fg}.{/center}');
    msg.setContent('{center}sending {green-fg}buy{/red-fg} to LP..{/center}');
    response.setContent('{center}waiting response..{/center}');

    /*
    var args = {
        data: { test: "hello" },
        headers: { "Content-Type": "application/json" }
    };
    
    baseURL = 'https://1broker.com/api/v1'
    apitoken = '62f188347a028f892a8570c9be41bc8e	'
    client.post("https://1broker.com/api/v1/account/overview.php?token="+apitoken+"&pretty=1", args, function (data, response) {
        // parsed response body as js object 
        console.log(data);
        // raw response 
        console.log(response);
        response.setContent(response);
    });*/
/*
    try {
    ai = oB.accountInfo();
    //console.log(ai);
    } catch(err) {

    }
*/
     /*setTimeout(function() {
        response.setContent('');
    }, 5000);*/
    screen.render();
});
// If box is focused, handle `enter` and give us some more content.
newTradeBuy.key('enter', function() {  
  newTradeBuy.setContent('{right}You pressed {black-fg}enter{/black-fg}.{/right}\n');
  newTradeBuy.setLine(1, 'bar');
  newTradeBuy.insertLine(1, 'foo');
  screen.render();
});


// ---
var newTradeSell = blessed.box({  
  parent: outer,
  top: '100',
  left: '500',
  width: '47.5%',
  height: '500',
  border: {
    type: '',
    fg: '#ffffff'
  },
  fg: 'white',
  bg: 'gray',
  content: '{bold}Sell{/bold}',
  tags: true,
  hoverEffects: {
    bg: '#aaaaaa'
  }
});
newTradeSell.on('click', function(data) {  
    //newTradeSell.setContent('{center}You clicked {red-fg}me{/red-fg}.{/center}');
    msg.setContent('{center}sending {red-fg}sell{/red-fg} to LP..{/center}');
    response.setContent('{center}waiting response..{/center}');
    setTimeout(function() {
        response.setContent('');
    }, 5000);
    screen.render();
});
// If box is focused, handle `enter` and give us some more content.
newTradeSell.key('enter', function() {  
  newTradeSell.setContent('{right}You pressed {black-fg}enter{/black-fg}.{/right}\n');
  newTradeSell.setLine(1, 'bar');
  newTradeSell.insertLine(1, 'foo');
  screen.render();
});

// ---
var msg = blessed.box({  
  parent: outer,
  top: '400',
  left: '10',
  width: '95%',
  height: '350',
  border: {
    type: '',
    fg: '#ffffff'
  },
  fg: 'white',
  bg: 'gray',
  content: '{bold}msg{/bold}',
  tags: true,
  /*hoverEffects: {
    bg: '#aaaaaa'
  }*/
});

var response = blessed.box({  
  parent: outer,
  top: '600',
  left: '10',
  width: '95%',
  height: '350',
  border: {
    type: '',
    fg: '#ffffff'
  },
  fg: 'white',
  bg: 'gray',
  content: '{bold}response{/bold}',
  tags: true,
  /*hoverEffects: {
    bg: '#aaaaaa'
  }*/
});




/*
// Create a child box perfectly centered horizontally and vertically.
var inner = blessed.box({  
  parent: outer,
  top: 'center',
  left: 'center',
  width: '50%',
  height: '50%',
  border: {
    type: 'line',
    fg: '#ffffff'
  },
  fg: 'white',
  bg: 'magenta',
  content: 'Click {bold}me{/bold}!',
  tags: true,
  hoverEffects: {
    bg: 'green'
  }
});

// If our box is clicked, change the content.
inner.on('click', function(data) {  
  inner.setContent('{center}You clicked {red-fg}me{/red-fg}.{/center}');
  screen.render();
});

// If box is focused, handle `enter` and give us some more content.
inner.key('enter', function() {  
  inner.setContent('{right}You pressed {black-fg}enter{/black-fg}.{/right}\n');
  inner.setLine(1, 'bar');
  inner.insertLine(1, 'foo');
  screen.render();
});

// Quit on Escape, q, or Control-C.
screen.key(['escape', 'q', 'C-c'], function(ch, key) {  
  return process.exit(0);
});

// Focus our element.
inner.focus();
*/

// Render the screen.
//screen.render(); 

var list = blessed.list({  
  parent: screen,
  width: '200',
  height: '50%',
  top: '10',
  left: '30',
  align: 'center',
  fg: 'white',
  border: {
    type: 'line'
  },
  selectedBg: 'green',

  // Allow mouse support
  mouse: true,

  // Allow key support (arrow keys + enter)
  keys: true,

  // Use vi built-in keys
  vi: true
});
list.setItems([  
  'EUR_USD',
  'GBP_USD',
]);
list.prepend(new blessed.Text({  
  left: 2,
  content: ' My list '
}));
// Allow scrolling with the mousewheel (manually).
list.on('wheeldown', function() {
  list.down();
});
list.on('wheelup', function() {
  list.up();
});
// Select the first item.
list.select(0);
list.on('click', function(data) {
  //console.log('test');  
});


// ----
var bias = blessed.list({  
  parent: screen,
  width: '200',
  height: '50%',
  top: '500',
  left: '30',
  align: 'center',
  fg: 'white',
  border: {
    type: 'line'
  },
  selectedBg: 'green',

  // Allow mouse support
  mouse: true,

  // Allow key support (arrow keys + enter)
  keys: true,

  // Use vi built-in keys
  vi: true
});
bias.setItems([  
  'Buy',
  'Sell',
]);
bias.prepend(new blessed.Text({  
  left: 2,
  content: ' My bias '
}));
// Allow scrolling with the mousewheel (manually).
bias.on('wheeldown', function() {
  bias.down();
});
bias.on('wheelup', function() {
  bias.up();
});
// Select the first item.
bias.select(0);
bias.on('click', function(data) {
  console.log('test');  
});


// ----
var risk = blessed.list({  
  parent: screen,
  width: '200',
  height: '50%',
  top: '500',
  left: '250',
  align: 'center',
  fg: 'white',
  border: {
    type: 'line'
  },
  selectedBg: 'green',

  // Allow mouse support
  mouse: true,

  // Allow key support (arrow keys + enter)
  keys: true,

  // Use vi built-in keys
  vi: true
});
risk.setItems([  
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
]);
risk.prepend(new blessed.Text({  
  left: 2,
  content: ' My risk '
}));
// Allow scrolling with the mousewheel (manually).
risk.on('wheeldown', function() {
  risk.down();
});
risk.on('wheelup', function() {
  risk.up();
  console.log('132');
});
// Select the first item.
risk.select(0);
risk.on('click', function(data) {
  console.log(data);
});


// ----
var liquidityProviders = blessed.list({  
  parent: screen,
  width: '200',
  height: '50%',
  top: '500',
  left: '500',
  align: 'center',
  fg: 'white',
  border: {
    type: 'line'
  },
  selectedBg: 'green',

  // Allow mouse support
  mouse: true,

  // Allow key support (arrow keys + enter)
  keys: true,

  // Use vi built-in keys
  vi: true
});
liquidityProviders.setItems([  
  'Oanda',
  '1broker',
]);
liquidityProviders.prepend(new blessed.Text({  
  left: 2,
  content: ''
}));
// Allow scrolling with the mousewheel (manually).
liquidityProviders.on('wheeldown', function() {
  liquidityProviders.down();
});
liquidityProviders.on('wheelup', function() {
  liquidityProviders.up();
  console.log('132');
});
// Select the first item.
liquidityProviders.select(0);
liquidityProviders.on('click', function(data) {
  console.log(data);
});


screen.key('q', function(ch, key) {  
  return process.exit(0);
});

screen.render(); 
