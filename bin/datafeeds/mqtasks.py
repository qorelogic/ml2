from celery import Celery
import time

app = Celery()

@app.task
def appendCsv(csvline, fname):
    #fp = open('{0}/{1}.csv'.format(self.hdir, pair), 'a')
    fp = open(fname, 'a')
    fp.write(csvline+'\n')
    #fp.write(csvline+'.mqtest\n')
    fp.close()
    #time.sleep(1)
    ''
    