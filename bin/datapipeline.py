
#import numpy as n
#from random import randint
#import threading

from qore import QoreDebug

from qore import DataPipeline

qd = QoreDebug()
qd.on()

try:
	dp = DataPipeline()
	#dp.z.send('we')
	df = dp.populateTickers(1, num=10)
	df
except:
	qd.printTraceBack()
	

