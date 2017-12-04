# source: http://ryanuber.com/04-29-2010/simple-puppet-cron-management.html
# cheatsheet: http://bencane.com/2012/09/03/cheat-sheet-crontab-by-example/
# source: http://ryanuber.com/04-29-2010/simple-puppet-cron-management.html
class r21 {
	cron { "r21":
	    #command => "nice -15 /mldev/bin/go.sh bitmex.py r21 2>&1 >> /tmp/go.log",
	    command => "nice -15 /mldev/bin/go.sh bitmex.py r21",
	    user    => "qore",
	    minute  => ['*/1']
	}
}
include r21
