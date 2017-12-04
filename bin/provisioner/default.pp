
#Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

# apt-get install python3-tk
# apt-get install tk-dev
# libsqlite3-dev
# sqlite3
# python-sqlite
# sqlite3-dev
# python-gtk2-dev

###############################################################################
### Start config ##############################################################
###############################################################################
$hdir        = "/mldev"
$installHdir = "$hdir/lib/ml"
$h2oHdir     = "$installHdir/h2o"
$sparkHdir   = "$installHdir/spark"
$sparklingWaterHdir   = "$installHdir/spark"

$pipbin = "/usr/bin/pip"
#$pipbin = "/usr/local/bin/pip"

### H2O #######################################################################
#$version_h2o      = "3.0.1.7"
#$codename_h2o     = "simons"
#$minor_h2o        = "7"

#$version_h2o     = "3.6.0.8"
#$codename_h2o    = "tibshirani"
#$minor_h2o       = "8"

#$version_h2o     = "3.8.0.4"
#$codename_h2o    = "tukey"
#$minor_h2o       = "4"

$version_h2o     = "3.10.1.1"
$codename_h2o    = "turnbull"
$minor_h2o       = "1"

$h2oTarball       = "http://h2o-release.s3.amazonaws.com/h2o/rel-$codename_h2o/$minor_h2o/h2o-$version_h2o.zip"

### Spark #####################################################################
$version_spark    = "1.4.0-bin-hadoop2.4"
$sparkTarball     = "http://d3kbcqa49mib13.cloudfront.net/spark-$version_spark.tgz"

### SparklingWater ############################################################
$version_sparklingWater_major = "1.4"
$version_sparklingWater_minor = "3"
$version_sparklingWater       = "$version_sparklingWater_major.$version_sparklingWater_minor"
$sparklingWaterTarball        = "http://h2o-release.s3.amazonaws.com/sparkling-water/rel-$version_sparklingWater_major/$version_sparklingWater_minor/sparkling-water-$version_sparklingWater.zip"

###############################################################################
### End config ################################################################
###############################################################################




class xrdp {

  $sysPackages = [ "xfce4", "xrdp" ]
  package { $sysPackages:
    ensure => "installed",
    #require => Exec['apt-get update'],
    before  => Exec["setXsession"],
  }
  exec { 'setXsession':
    command => '/bin/cp -p /mldev/bin/provisioner/dot.xsession /home/qore/.xsession',
    before  => Exec["restart xrdp"],
  }
  exec { 'restart xrdp':
    command => '/etc/init.d/xrdp restart',
  }
}

class qpackages {
  package { "wipe":
    ensure  => present,
    require => Class["system-update"],
  }
}

class apache {
  package { "apache2":
    ensure  => present,
    require => Class["system-update"],
  }

  service { "apache2":
    ensure  => "running",
    require => Package["apache2"],
  }

}

class unzip {
  package { "unzip":
    ensure  => present,
    require => Class["system-update"],
  }
}

class curl {
  package { "curl":
    ensure  => present,
    require => Class["system-update"],
  }
}

class portmap {
    #package { "portmap":
    #ensure  => present,
    #require => Class["system-update"],
    #}
    $sysPackages = [ "portmap" ]
    package { $sysPackages:
        ensure => "installed",
        require => Exec['apt-get update'],
    }
}

# https://www.tensorflow.org/versions/0.6.0/get_started/os_setup.html#pip_install
class tensorflow {
	#sudo pip install sklearn
	exec { "pip install sklearn":
		command => "$pipbin install sklearn",
		timeout => 60,
		tries   => 3,
	}
	#sudo pip install jupyter
	exec { "pip install jupyter":
		command => "$pipbin install jupyter",
		timeout => 60,
		tries   => 3,
	}
	exec { "pip install tensorflow":
		command => "$pipbin install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl",
		timeout => 60,
		tries   => 3,
	}
	# git clone https://github.com/tensorflow/tensorflow
	exec { "git clone tensorflow":
		command => "/usr/bin/git clone https://github.com/tensorflow/tensorflow /mldev/lib/ml/tensorflow",
		timeout => 300,
		tries   => 3,
		before  => Exec["git clone tensorflow2"],
	}
	exec { "git clone tensorflow2":
		command => "/bin/chown -R qore: /mldev/lib/ml/tensorflow",
		timeout => 300,
		tries   => 3,
	}
}


class datafeeds {

#MPWD=`pwd`

#mlocal=~/.tmuxifier
#mldir=/ml.dev

#mdependencies() {
#	sleep 1
#	echo ''
#	echo -n 'Need to install tmuxifier..  '
#	sleep 3
#	echo ' ..installing..'
#	echo ''
#	sleep 3
#	git clone https://github.com/jimeh/tmuxifier.git $mlocal
#
#	echo ''
#	echo 'dependencies complete.'

#}

#minstall() {

	#sleep 1
	#if [ "`which puppet`" == "" ]; then
     #       sudo apt-get update
     #       sudo apt-get -y install puppet
	#fi
	#if [ ! -f $mlocal/layouts/qlm.window.sh ]; then
	#	echo "$mlocal/layouts contents:"
	#	ls -l $mlocal/layouts
	#	echo "need to fix $mlocal/layouts, sure you want to remove directory $mlocal/layouts? y/n: "
	#	read ans
	#	if [ "$ans" == "y" ]; then
	#		rm -r $mlocal/layouts
	#		rm -rfv $mlocal/layouts
	#		ln -s $mldir/bin/tmuxifier/layouts $mlocal/layouts 2> /dev/null
	#		echo 'linked mldev/bin/tmuxifier/layouts to ~/.tmuxifier/layouts'
	#	fi
	#fi
	#if [ ! -f $mldir/lib/oanda/oandapy/oandapy.py ]; then
	#	mkdir -p $mldir/lib/oanda/
	#	echo 'oandapy'
	#	git clone https://github.com/oanda/oandapy.git /ml.dev/lib/oanda/oandapy
	#	echo 'cloned oandapy.'
	#fi
	#if [ "`echo $PYTHONPATH | grep -i oandapy`" == "" ]; then
	#	export PYTHONPATH=$PYTHONPATH:/ml.dev/lib/oanda/oandapy
	#	echo 'adding path to Python path '
	#fi
	#if [ "`cat ~/.bashrc | grep -i oandapy`" == "" ]; then
	#	echo 'export PYTHONPATH=$PYTHONPATH:/ml.dev/lib/oanda/oandapy' >> ~/.bashrc
	#	echo 'adding PYTHONPATH export ~/.bashrc'
	#fi
	#if [ ! -f $mldir/lib/bitcoin/localbitcoins/digithink_py-localbitcoins.github.py.git ]; then
	#	mkdir -p $mldir/lib/bitcoin/localbitcoins/
	#	echo 'py-localbitcoins'
	#	git clone https://github.com/digithink/py-localbitcoins.git $mldir/lib/bitcoin/localbitcoins/digithink_py-localbitcoins.github.py.git
	#	echo 'cloned py-localbitcoins.'
	#fi
	exec { "pip install drest": command => "$pipbin install drest==0.9.12", timeout => 60, tries => 3 }
	#if [ ! -f $mldir/lib/bitcoin/1broker/aol1306_1broker-trading-API.github.py.git ]; then
	#	mkdir -p $mldir/lib/bitcoin/1broker/
	#	echo 'API1brokerlib'
	#	git clone https://github.com/aol1306/1broker-trading-API.git $mldir/lib/bitcoin/1broker/aol1306_1broker-trading-API.github.py.git
	#	echo 'cloned API1brokerlib.'
	#fi

	#sudo pip install --upgrade pip
	#exec { "pip install ipython":
	#	command => "if [ "`python -c 'import ipython' 2>&1`" != "" ]; then $pipbin install ipython; fi",
	#	timeout => 60,
	#	tries   => 3,
	#}
	exec { "pip install requests": command => "$pipbin install requests", timeout => 60, tries => 3 }
	exec { "pip install requests[security]": command => "$pipbin install requests[security]", timeout => 60, tries => 3 }
        # removes the security warning "A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL"
	exec { "pip install upgrade requests ssl security": command => "$pipbin install --upgrade pyopenssl ndg-httpsclient pyasn1 pip", timeout => 60, tries => 3 }

	exec { "pip install ipython": command => "$pipbin install ipython==4.0.3", timeout => 60, tries => 3 }
	exec { "pip install notebook": command => "$pipbin install notebook==4.1.0", timeout => 60, tries => 3 }
	exec { "pip install numpy": command => "$pipbin install numpy==1.9.2", timeout => 60, tries => 3 }
	exec { "pip install pandas": command => "$pipbin install pandas==0.15.2", timeout => 60, tries => 3 }
	exec { "pip install plotly": command => "$pipbin install plotly==1.6.10", timeout => 60, tries => 3 }
	exec { "pip install ujson": command => "$pipbin install ujson==1.33", timeout => 60, tries => 3 }
	#if [ "`python -c 'import digitalocean' 2>&1`" != "" ]; then
     #       sudo pip install python-digitalocean
	#fi
	exec { "pip install python-digitalocean": command => "$pipbin install python-digitalocean==1.6", timeout => 60, tries => 3 }
	exec { "pip install vultr": command => "$pipbin install vultr==0.1.2", timeout => 60, tries => 3 }
	exec { "pip install QSTK": command => "$pipbin install QSTK==0.2.8", timeout => 60, tries => 3 }
	exec { "pip install Quandl": command => "$pipbin install Quandl==1.5", timeout => 60, tries => 3 }
	exec { "pip install html2text": command => "$pipbin install html2text==2014.12.29", timeout => 60, tries => 3 }
	exec { "pip install selenium": command => "$pipbin install selenium==2.45.0", timeout => 60, tries => 3 }

	# Mongo
	exec { "pip install pymongo": command => "$pipbin install pymongo", timeout => 60, tries => 3 }

	# MQ
	#if [ "`python -c 'import zmq' 2>&1`" != "" ]; then
     #       sudo pip install pyzmq
	#fi
	exec { "pip install pyzmq": command => "$pipbin install pyzmq==14.0.1", timeout => 60, tries => 3 }
	#if [ "`python -c 'import tailf' 2>&1`" != "" ]; then
     #       sudo pip install pytailf
	#fi
	exec { "pip install pytailf": command => "$pipbin install pytailf==1.1", timeout => 60, tries => 3 }
	exec { "pip install flask": command => "$pipbin install flask==0.10.1", timeout => 60, tries => 3 }
	exec { "pip install celery": command => "$pipbin install celery==3.1.17", timeout => 60, tries => 3 }

	# still testing on ipython notebook
	exec { "pip install bitstampy": command => "$pipbin install bitstampy==0.0.8", timeout => 60, tries => 3 }
	exec { "pip install krakenex": command => "$pipbin install krakenex", timeout => 60, tries => 3 }

	#echo ''
	#echo 'install complete.'
#}

#if [ -d $mlocal ]; then
#	minstall
#else
#	mdependencies
#	minstall
#fi


}

# source: http://stackoverflow.com/questions/11327582/puppet-recipe-installing-tarball
class h2o {
	#sudo pip install h2o
	exec { "pip uninstall h2o":
		command => "$pipbin uninstall h2o",
		timeout => 60,
		tries   => 3,
		before  => Exec["pip install h2o"],
	}
	exec { "pip install h2o":
		command => "$pipbin install http://h2o-release.s3.amazonaws.com/h2o/rel-$codename_h2o/$minor_h2o/Python/h2o-$version_h2o-py2.py3-none-any.whl",
		timeout => 60,
		tries   => 3,
	}

	exec { "mkdir_${h2oHdir}": command => "/bin/mkdir -p $h2oHdir" }
	exec { "wget_${h2oTarball}":
		command => "/usr/bin/wget -nc $h2oTarball -P $h2oHdir/",
		#command => "wget -nc $h2oTarball",
		#cwd => "$h2oHdir",
		timeout => 60,
		tries   => 3,
		#refreshonly => true,
		#notify => Exec['unzip h2o'],
		before  => Exec["unzip h2o"],
	}
	exec { 'unzip h2o': 
		command => "/usr/bin/unzip -o $h2oHdir/h2o-$version_h2o.zip -d $h2oHdir/", 
		#cwd => "$h2oHdir",
		timeout => 60, 
		tries   => 3,
		require => Class["unzip"],
	}
	#exec { 'run h2o':      command => "java -jar $h2oHdir/h2o-$version_h2o/h2o.jar",      timeout => 5, tries   => 3 }
}

# source: 
class openflights {
	exec { "mkdir_openflights": 
		command => "mkdir -p /mldev/lib/crawlers/transport/",
		before  => Exec["gitclone_openflights"],
     }
	exec { "gitclone_openflights":
		command => "git clone https://github.com/jpatokal/openflights.git /mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git",
		timeout => 60,
		tries   => 3,
		#refreshonly => true,
		before  => Exec["unzip openflights"],
	}
	exec { 'unzip openflights': 
		command => "unzip -o /mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git/data/DAFIFT_0610_ed6.zip -d /mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git/data/DAFIFT_0610_ed6", 
		timeout => 60, 
		tries   => 3,
		require => Class["unzip"],
	}
}

class sparkling-water {
	exec { "mkdir $sparklingWaterHdir": command => "mkdir -p $sparklingWaterHdir" }
	exec { "bashrc touch":
		command => "echo \"export SPARK_HOME='/home/qore/mldev/lib/ml/spark/spark-$version_spark'\" >> /home/qore/.bashrc",
		before  => Exec["wget $sparklingWaterTarball"],
	}
	exec { "wget $sparklingWaterTarball":
		command => "wget -nc $sparklingWaterTarball -P $sparklingWaterHdir/",
		#command => "wget -nc $sparklingWaterTarball",
		#cwd => "$sparklingWaterHdir",
		timeout => 60,
		tries   => 3,
		#creates => "$sparklingWaterHdir/sparkling-water-$version_sparklingWater.zip",
		#refreshonly => true,
		#notify => Exec['unzip sparkling'],
		before  => Exec["unzip sparkling"],
	}
	exec { 'unzip sparkling': 
		command => "unzip -o $sparklingWaterHdir/sparkling-water-$version_sparklingWater.zip -d $sparklingWaterHdir/", 
		#command => "/usr/bin/unzip -o $sparklingWaterHdir/sparkling-water-$version_sparklingWater.zip",
		#cwd => "$sparklingWaterHdir",
		timeout => 60, 
		tries   => 3,
		require => Class["unzip"],
	}
	#exec { 'run sparkling':      command => "$sparklingWaterHdir/sparkling-water-$version_sparklingWater/bin/sparkling-shell",      timeout => 5, tries   => 3 }
}

class spark {
	exec { "mkdir -p $sparkHdir": command => "mkdir -p $sparkHdir" }
	exec { "wget -nc $sparkTarball":
		command => "wget -nc $sparkTarball -P $sparkHdir/",
		timeout => 60,
		tries   => 3,
		before  => Exec["untar spark"],
	}
	exec { 'untar spark': 
		command => "tar zxf $sparkHdir/spark-$version_spark.tgz -C $sparkHdir/", 
		timeout => 60, 
		tries   => 3,
		#require => File["$sparkHdir/spark-$version_spark.tgz"],
	}
	#exec { 'run spark':      command => "$sparkHdir/spark-$version_spark/bin/spark-shell",        timeout => 60, tries   => 3 }
}

class numba {
     exec { "llvm-3.6":    command => "apt-get install llvm-3.6",        timeout => 60, tries   => 3, before  => Exec["llvm-3.6-dev"] }
     exec { "llvm-3.6-dev": command => "apt-get install llvm-3.6-dev",    timeout => 60, tries   => 3, before  => Exec["enum34"] }
     exec { "enum34":      command => "pip     install enum34==1.1.6",   timeout => 60, tries   => 3, before  => Exec["zlib1g-dev"] }
     exec { "zlib1g-dev":  command => "apt-get install zlib1g-dev",      timeout => 60, tries   => 3, before  => Exec["libedit-dev"] }
     exec { "libedit-dev": command => "apt-get install libedit-dev",     timeout => 60, tries   => 3, before  => Exec["llvmlite"] }
     # http://stackoverflow.com/questions/29041356/how-to-point-llvm-config-environment-variable-to-the-path-for-llvm-config
     exec { "llvmlite":    command => "LLVM_CONFIG=`which llvm-config-3.6` pip install llvmlite==0.8.0", timeout => 60, tries   => 3, before  => Exec["numba"] }
     exec { "numba":       command => "pip     install numba==0.23.0",   timeout => 60, tries   => 3 }
}

class keys {
	exec { 'run node':      command => "cat /home/qore/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys",        timeout => 60, tries   => 3 }
}

# source: http://ryanuber.com/04-29-2010/simple-puppet-cron-management.html
# cheatsheet: http://bencane.com/2012/09/03/cheat-sheet-crontab-by-example/
# source: http://ryanuber.com/04-29-2010/simple-puppet-cron-management.html
class crontab {
	cron { "logEquity":
	    command => "python /mldev/bin/logEquity.py",
	    user    => "qore",
	    #hour    => 0,
	    #minute  => 0,
	    weekday  => [0,1,2,3,4,5]
	}
	cron { "dataminer":
	    command => "nice -15 /mldev/bin/dataminer.sh",
	    user    => "qore",
	    minute  => [0,15,30,45]
	}
	cron { "dataminerInvestingWorldGovernmentBonds":
	    command => "nice -15 /mldev/bin/dataminerInvestingWorldGovernmentBonds.sh",
	    user    => "qore",
	    minute  => [0,5,10,15,20,25,30,35,40,45,50,55]
	}
}

import 'crontab.pp'
include r21

import 'system-update.pp'
#import 'cassandra.pp'
import 'javart.pp'
import 'mongodb.pp'

#import 'trac.pp'
#include trac

include datafeeds
#include numba

#include cassandra
import 'nfs-server.pp'
import 'nfs-client.pp'

include qpackages
#include apache

include portmap
include nfs-server
include nfs-client
include unzip
include curl
include javart
#include h2o
include tensorflow
#include spark
#include sparkling-water
#include crontab
#import 'nodejs.pp'
#include nodejs
#import 'talib.pp'
#include talib
include xrdp
#include keys
#include openflights
