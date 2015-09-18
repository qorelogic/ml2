
from flask import Flask, url_for
from flask import render_template

from oandaq import OandaQ
#from qorequant import QoreQuant

oq = OandaQ()
#qq = QoreQuant()

app = Flask(__name__)

import socket, fcntl, struct
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
#get_ip_address('eth0')  # '192.168.0.110'

#import socket
#def get_ip_address():
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.connect(("8.8.8.8", 80))
#    return s.getsockname()[0]  
#get_ip_address()

#@app.route('/')
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    #return "Hello World!"
    return render_template('hello.html', name=name)

@app.route('/')
@app.route('/zmq/')
@app.route('/zmq/<name>')
def zmq(name=None):
    #import ujson as j
    pairs = oq.getBabySitPairs()#.split(',')
    #print pairs
    #pairs = j.dumps(pairs)
    liquid_ipaddr=get_ip_address('eth0')
    return render_template('zmq-client.html', name=name, liquid_ipaddr=liquid_ipaddr, pairs=pairs)
    
if __name__ == '__main__':

    #ADMINS = ['yourname@example.com']
    import logging
    #from logging.handlers import SMTPHandler
    #mail_handler = SMTPHandler('127.0.0.1',
    #                           'server-error@example.com',
    #                           ADMINS, 'YourApplication Failed')
    #mail_handler.setLevel(logging.ERROR)
    #app.logger.addHandler(mail_handler)
    """
    from logging.handlers import FileHandler
    file_handler = FileHandler('/tmp/zmq-client.flask.py.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    """

    from logging import StreamHandler
    import sys
    file_handler = StreamHandler(sys.stdout)
    file_handler.setLevel(logging.DEBUG)
    #file_handler.setLevel(logging.INFO)
    #file_handler.setLevel(logging.WARNING)
    #file_handler.setLevel(logging.ERROR)
    #file_handler.setLevel(logging.CRITICAL)
    app.logger.addHandler(file_handler)

    app.run(host='0.0.0.0')
    url_for('static', filename='style.css')
