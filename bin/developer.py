#!/usr/bin/python

import argparse
from crontab import CronTab

# source: https://wuilly.com/2012/05/15/manage-cron-jobs-with-python-crontab/
"""
Here the object can take two parameters one for setting 
the user cron jobs, it defaults to the current user 
executing the script if ommited. The fake_tab parameter 
sets a testing variable. So you can print what could be 
written to the file onscreen instead or writting directly
into the crontab file. 
"""

# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
#parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-on", '--on',   help="go live    and turn on",         action="store_true")
parser.add_argument("-off", '--off', help="go offline and turn off", action="store_true")
parser.add_argument("-l", '--list', help="go offline and turn off", action="store_true")
parser.add_argument("-v", '--view', help="go offline and turn off", action="store_true")
parser.add_argument("-p", '--project', help="set the project name")
args = parser.parse_args()

#tab = CronTab(user='www',fake_tab='True')
tab = CronTab(user='qore')
if args.project:
    cmd = '/mldev/bin/logDeveloper.sh %s' %  args.project

def usage():
    print 'usage: [-on|-off] -p <project name>'

import re
def developerLogOff():
    # delete crontable
    #cron_job = tab.find_command(cmd)
    #print cron_job.next()
    #print 

    #tab.remove_all()
    for i in range(len(tab.crons)):
        try:
            manifest = tab.crons[i]
            groups = re.match(re.compile(r'.*(Developer).*', re.S), str(manifest)).groups()
            # throws exception if this cron is not of type Developer, otherwise delete this cron.
            manifest.delete()
        except Exception as e:
            #print e
            ''
    tab.write()
    
    #tab.write()
    #print tab.render()
    
def developerLogOn():

    li = []
    for i in range(len(tab.crons)):
        try:
            groups = re.match(re.compile(r'.*(Developer).*', re.S), str(tab.crons[i])).groups()        
            li.append(1)
        except Exception as e:
            #print e
            ''
    if len(li) == 0:
        # You can even set a comment for this command
        cron_job = tab.new(cmd, comment='Developer Log')
        #cron_job.minute().every(5)
        cron_job.minute.every(1)
        #cron_job.hour.on(12)
        #writes content to crontab
        tab.write()
        #print tab.render()

def viewList():
    cmd = 'ls /mldev/screenshots/developerLogs/screen/%s/qore/' % args.project
    #cmd = 'ls /'
    import subprocess as sp
    import pandas as p
    import datetime as dd
    li = sp.check_output(cmd.split(' ')).split('\n')
    df = p.DataFrame(li)
    df.ix[0:len(df.index)-2,1] = map(lambda x: x.split('-')[3].split('.')[0], df.ix[0:len(df.index)-2,0])
    df[1] = p.to_numeric(df[1])
    df.ix[0:len(df.index)-2,2] = map(lambda x: dd.datetime.fromtimestamp(x).strftime('%Y%m%d-%H%M%S'), df.ix[0:len(df.index)-2,1])
    df = df.sort_values(by=1)
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #print df.dtypes
        print df#.tail(10)

if args.project:
    if args.on:
        #developerLogOff()
        developerLogOn()
    
    if args.off:
        developerLogOff()
    
    if args.list:
        tab = CronTab(user='qore')
        print tab.render()
        
    if args.view:
        viewList()
else:
    usage()
