
import zmq, time

ctx = zmq.Context()
#socket = ctx.socket(zmq.REP)
#socket = ctx.socket(zmq.PUSH)
socket = ctx.socket(zmq.PUB);
socket.bind('tcp://*:5555')

c = 0
while True:
    #socket.recv(0) # only for REP
    stri = 'world {0}'.format(c)
    #print stri
    topic = 'tester'
    socket.send("%s %s" % (topic, stri)) # only for PUB
    #socket.send(stri)
    c += 1
    time.sleep(0.1)
