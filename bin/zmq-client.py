
import zmq, time, sys

# option to change the port number from default 5555
try:
    port = sys.argv[1]
except:
    port = 5555    

ctx = zmq.Context()
#socket = ctx.socket(zmq.REQ)
socket = ctx.socket(zmq.SUB)
socket.connect('tcp://localhost:{0}'.format(port))


# Subscribe to tester
topicfilter = 'tester'
#socket.subscribe(topicfilter) # only for SUB
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

c = 0
while True:
    #socket.send('test client') # only for REQ
    print socket.recv(0).split(' ')[1]
    c += 1
    #time.sleep(0.1)
