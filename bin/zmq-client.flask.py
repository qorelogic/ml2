
from flask import Flask, url_for
from flask import render_template

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

    liquid_ipaddr=get_ip_address('eth0')
    return render_template('zmq-client.html', name=name, liquid_ipaddr=liquid_ipaddr)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    url_for('static', filename='style.css')
