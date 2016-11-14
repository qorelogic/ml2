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
args = parser.parse_args()

#tab = CronTab(user='www',fake_tab='True')
tab = CronTab(user='qore')
cmd = '/mldev/bin/logDeveloper.sh'

def developerLogOff():
    # delete crontable
    cron_job = tab.find_command(cmd)
    #print cron_job.next()
    #print 
    tab.remove_all()
    tab.write()
    #print tab.render()
    
def developerLogOn():
    # You can even set a comment for this command
    cron_job = tab.new(cmd, comment='Developer Log')
    #cron_job.minute().every(5)
    cron_job.minute.every(1)
    #cron_job.hour.on(12)
    #writes content to crontab
    tab.write()
    #print tab.render()

if args.on:
    developerLogOff()
    developerLogOn()

if args.off:
    developerLogOff()

if args.list:
    print tab.render()
