
from flask import Flask, url_for
from flask import render_template

app = Flask(__name__)

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
    #return "Hello World!"
    return render_template('zmq-client.html', name=name)
    
if __name__ == '__main__':
    app.run()
    url_for('static', filename='style.css')
