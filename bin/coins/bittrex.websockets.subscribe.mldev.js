
// print process.argv
/*process.argv.forEach(function (val, index, array) {
  console.log(index + ': ' + val);
});*/

// source: https://stackoverflow.com/questions/29907608/zmq-pub-sub-subscribe

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

if (process.argv.length > 2) {
  pairs = [process.argv[2]];
}
else {
  pairs = 'BTC-LTC,BTC-DOGE,BTC-VTC,BTC-PPC,BTC-FTC,BTC-RDD,BTC-NXT,BTC-DASH,BTC-POT,BTC-BLK,BTC-EMC2,BTC-MYR,BTC-AUR,BTC-EFL,BTC-GLD,BTC-SLR,BTC-PTC,BTC-GRS,BTC-NLG,BTC-RBY,BTC-XWC,BTC-MONA,BTC-THC,BTC-ENRG,BTC-ERC,BTC-NAUT,BTC-VRC,BTC-CURE,BTC-XBB,BTC-XMR,BTC-CLOAK,BTC-START,BTC-KORE,BTC-XDN,BTC-TRUST,BTC-NAV,BTC-XST,BTC-BTCD,BTC-VIA,BTC-UNO,BTC-PINK,BTC-IOC,BTC-CANN,BTC-SYS,BTC-NEOS,BTC-DGB,BTC-BURST,BTC-EXCL,BTC-SWIFT,BTC-DOPE,BTC-BLOCK,BTC-ABY,BTC-BYC,BTC-XMG,BTC-BLITZ,BTC-BAY,BTC-BTS,BTC-FAIR,BTC-SPR,BTC-VTR,BTC-XRP,BTC-GAME,BTC-COVAL,BTC-NXS,BTC-XCP,BTC-BITB,BTC-GEO,BTC-FLDC,BTC-GRC,BTC-FLO,BTC-NBT,BTC-MUE,BTC-XEM,BTC-CLAM,BTC-DMD,BTC-GAM,BTC-SPHR,BTC-OK,BTC-SNRG,BTC-PKB,BTC-CPC,BTC-AEON,BTC-ETH,BTC-GCR,BTC-TX,BTC-BCY,BTC-EXP,BTC-INFX,BTC-OMNI,BTC-AMP,BTC-AGRS,BTC-XLM,BTC-BTA,USDT-BTC,BITCNY-BTC,BTC-CLUB,BTC-VOX,BTC-EMC,BTC-FCT,BTC-MAID,BTC-EGC,BTC-SLS,BTC-RADS,BTC-DCR,BTC-SEC,BTC-BSD,BTC-XVG,BTC-PIVX,BTC-XVC,BTC-MEME,BTC-STEEM,BTC-2GIVE,BTC-LSK,BTC-PDC,BTC-BRK,BTC-DGD,ETH-DGD,BTC-WAVES,BTC-RISE,BTC-LBC,BTC-SBD,BTC-BRX,BTC-DRACO,BTC-ETC,ETH-ETC,BTC-STRAT,BTC-UNB,BTC-SYNX,BTC-TRIG,BTC-EBST,BTC-VRM,BTC-SEQ,BTC-XAUR,BTC-SNGLS,BTC-REP,BTC-SHIFT,BTC-ARDR,BTC-XZC,BTC-ANS,BTC-ZEC,BTC-ZCL,BTC-IOP,BTC-DAR,BTC-GOLOS,BTC-HKG,BTC-UBQ,BTC-KMD,BTC-GBG,BTC-SIB,BTC-ION,BTC-LMC,BTC-QWARK,BTC-CRW,BTC-SWT,BTC-TIME,BTC-MLN,BTC-ARK,BTC-DYN,BTC-TKS,BTC-MUSIC,BTC-DTB,BTC-INCNT,BTC-GBYTE,BTC-GNT,BTC-NXC,BTC-EDG,BTC-LGD,BTC-TRST,ETH-GNT,ETH-REP,USDT-ETH,ETH-WINGS,BTC-WINGS,BTC-RLC,BTC-GNO,BTC-GUP,BTC-LUN,ETH-GUP,ETH-RLC,ETH-LUN,ETH-SNGLS,ETH-GNO,BTC-APX,BTC-TKN,ETH-TKN,BTC-HMQ,ETH-HMQ,BTC-ANT,ETH-TRST,ETH-ANT,BTC-SC,ETH-BAT,BTC-BAT,BTC-ZEN,BTC-1ST,BTC-QRL,ETH-1ST,ETH-QRL,BTC-CRB,ETH-CRB,ETH-LGD,BTC-PTOY,ETH-PTOY,BTC-MYST,ETH-MYST,BTC-CFI,ETH-CFI,BTC-BNT,ETH-BNT,BTC-NMR,ETH-NMR,ETH-TIME,ETH-LTC,ETH-XRP,BTC-SNT,ETH-SNT,BTC-DCT,BTC-XEL,BTC-MCO,ETH-MCO,BTC-ADT,ETH-ADT,BTC-FUN,ETH-FUN,BTC-PAY,ETH-PAY,BTC-MTL,ETH-MTL,BTC-STORJ,ETH-STORJ,BTC-ADX,ETH-ADX,ETH-DASH,ETH-SC,ETH-ZEC,USDT-ZEC,USDT-LTC,USDT-ETC,USDT-XRP,BTC-OMG,ETH-OMG,BTC-CVC,ETH-CVC,BTC-PART,BTC-QTUM,ETH-QTUM,ETH-XMR,ETH-XEM,ETH-XLM,ETH-ANS,USDT-XMR,USDT-DASH'.split(',')
  //pairs = ['BTC-ETH','BTC-SC','BTC-ZEN']
  //pairs = ['BTC-ETH']
  //pairs = ['BTC-RDD']
  //pairs = ['BTC-TKS']
  //pairs = ['BTC-BTCD']
}

const websocketsclient = bittrex.websockets.subscribe(pairs, function(data) {
  if (data.M === 'updateExchangeState') {
    data.A.forEach(function(data_for) {
      //console.log('Market Update for '+ data_for.MarketName, data_for);
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
