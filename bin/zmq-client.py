
import zmq, time

ctx = zmq.Context()
#socket = ctx.socket(zmq.REQ)
socket = ctx.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')


# Subscribe to tester
topicfilter = 'tester'
#socket.subscribe(topicfilter) # only for SUB
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

c = 0
while True:
    #socket.send('test client') # only for REQ
    print socket.recv(0)
    c += 1
    #time.sleep(0.1)
