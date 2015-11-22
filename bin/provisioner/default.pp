
#Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

$hdir        = "/mldev"
$installHdir = "$hdir/lib/ml"
$h2oHdir     = "$installHdir/h2o"
$sparkHdir   = "$installHdir/spark"
$sparklingWaterHdir   = "$installHdir/spark"

$version_h2o      = "3.0.1.7"
#$version_h2o     = "3.6.0.8"
$version_spark    = "1.4.0-bin-hadoop2.4"

$version_sparklingWater_major = "1.4"
$version_sparklingWater_minor = "3"
$version_sparklingWater       = "$version_sparklingWater_major.$version_sparklingWater_minor"


$h2oTarball   = "http://h2o-release.s3.amazonaws.com/h2o/rel-simons/7/h2o-$version_h2o.zip"
$sparkTarball = "http://d3kbcqa49mib13.cloudfront.net/spark-$version_spark.tgz"
$sparklingWaterTarball = "http://h2o-release.s3.amazonaws.com/sparkling-water/rel-$version_sparklingWater_major/$version_sparklingWater_minor/sparkling-water-$version_sparklingWater.zip"

$nodeV           = "node-v4.1.0-linux-x64"
$nodeTarball     = "$nodeV.tar.gz"
$nodeTarballURL  = "https://nodejs.org/dist/latest/$nodeTarball"
$nodeHdir        = "$installHdir/node"

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
	#sudo apt-get install python-scipy
	$sysPackages = [ "python-scipy", 'ipython', 'ipython-notebook', 'python-matplotlib', 'python-tk', 'python-pil' ]
	package { $sysPackages:
		ensure => "installed",
		require => Exec['apt-get update'],
	}
	#sudo pip install sklearn
	exec { "pip install sklearn":
		command => "/usr/local/bin/pip install sklearn",
		timeout => 60,
		tries   => 3,
	}
	#sudo pip install jupyter
	exec { "pip install jupyter":
		command => "/usr/local/bin/pip install jupyter",
		timeout => 60,
		tries   => 3,
	}
	exec { "pip install tensorflow":
		command => "/usr/local/bin/pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl",
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
		command => "chown -R qore: /mldev/lib/ml/tensorflow",
		timeout => 300,
		tries   => 3,
	}
}

# source: http://stackoverflow.com/questions/11327582/puppet-recipe-installing-tarball
class h2o {
	#sudo pip install h2o
	exec { "pip install h2o":
		command => "/usr/local/bin/pip install h2o",
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
		command => "mkdir -p /mldev/lib/crawlers/transport/"
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

class nodejs {
	exec { "mkdir -p $nodeHdir": command => "mkdir -p $nodeHdir" }
	exec { "wget -nc $nodeTarball":
		command => "wget -nc $nodeTarballURL -P $nodeHdir/",
		timeout => 60,
		tries   => 3,
		before  => Exec["untar node"],
	}
	exec { 'untar node': 
		command => "tar zxf $nodeHdir/$nodeTarball -C $nodeHdir/", 
		timeout => 60, 
		tries   => 3,
		#require => File["$nodeHdir/$nodeTarball"],
		before  => Exec["rm node symlinks"],
	}
	exec { 'rm node symlinks':
		command => "rm -f /usr/bin/node; rm -f /usr/bin/npm;", 
		timeout => 60, 
		tries   => 3,
		before  => Exec["node symlinks"],
	}
	exec { 'node symlinks':
		command => "ln -s $nodeHdir/$nodeV/bin/node /usr/bin/node; ln -s $nodeHdir/$nodeV/bin/npm /usr/bin/npm;",
		timeout => 60, 
		tries   => 3,
	}
	#exec { 'run node':      command => "$nodeHdir/bin/node",        timeout => 60, tries   => 3 }
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

import 'system-update.pp'
#import 'cassandra.pp'
import 'javart.pp'
import 'mongodb.pp'

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
include h2o
include tensorflow
#include spark
#include sparkling-water
include crontab
#include nodejs
include xrdp
#include keys
#include openflights
