
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

$hdir        = "/mldev"
$installHdir = "$hdir/lib/ml"
$h2oHdir     = "$installHdir/h2o"
$sparkHdir   = "$installHdir/spark"
$sparklingWaterHdir   = "$installHdir/spark"

$h2oTarball   = "http://h2o-release.s3.amazonaws.com/h2o/rel-simons/7/h2o-3.0.1.7.zip"
$sparkTarball = "http://d3kbcqa49mib13.cloudfront.net/spark-1.4.0-bin-hadoop2.4.tgz"
$sparklingWaterTarball = "http://h2o-release.s3.amazonaws.com/sparkling-water/rel-1.4/3/sparkling-water-1.4.3.zip"

$nodeV           = "node-v4.1.0-linux-x64"
$nodeTarball     = "$nodeV.tar.gz"
$nodeTarballURL  = "https://nodejs.org/dist/latest/$nodeTarball"
$nodeHdir        = "$installHdir/node"

class system-update {
  exec { 'apt-get update':
    command => 'apt-get update',
  }

  $sysPackages = [ "build-essential" ]
  package { $sysPackages:
    ensure => "installed",
    require => Exec['apt-get update'],
  }
}

class xrdp {

  $sysPackages = [ "xfce4", "xrdp" ]
  package { $sysPackages:
    ensure => "installed",
    require => Exec['apt-get update'],
    before  => Exec["setXsession"],
  }
  exec { 'setXsession':
    command => 'cp -p /mldev/bin/provisioner/dot.xsession /home/qore/.xsession',
    before  => Exec["restart xrdp"],
  }
  exec { 'restart xrdp':
    command => '/etc/init.d/xrdp restart',
  }
}

import 'cassandra.pp'

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

class javart {
  package { "openjdk-8-jre-headless":
    ensure  => present,
    require => Class["system-update"],
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

class nfs-server {
    package { "nfs-kernel-server":
    ensure  => present,
    require => Class["system-update"],
    }
    #package { "portmap":
    #ensure  => present,
    #require => Class["system-update"],
    #}
    $sysPackages = [ "portmap" ]
    package { $sysPackages:
        ensure => "installed",
        require => Exec['apt-get update'],
    }
    exec { "mkdir_nfs_share}":
        command => "cat /etc/exports | grep -v '^/Opt/nfs'  | tee expo > /dev/null",
        timeout => 60,
        tries   => 3,
        #notify => Exec['unzip h2o'],
        before  => Exec["add2exports"],
    }
    exec { "add2exports}":
        command => "echo '/Opt/nfs  192.168.3.*(rw,sync,anonuid=1000,anongid=1000,all_squash)' >> expo",
        timeout => 60,
        tries   => 3,
        before  => Exec["nfs-kernel-server restart"],
    }
    exec { "nfs-kernel-server restart}":
        command => "service nfs-kernel-server restart",
        #command => "exportfs -a",
        timeout => 60,
        tries   => 3,
    }
}
class nfs-client {
    package { "nfs-common":
    ensure  => present,
    require => Class["system-update"],
    }
    #package { "portmap":
    #ensure  => present,
    #require => Class["system-update"],
    #}
    $sysPackages = [ "portmap" ]
    package { $sysPackages:
        ensure => "installed",
        require => Exec['apt-get update'],
    }
    exec { "mkdir_nfs_share}":
        command => "mkdir /mnt/nfs-share",
        #cwd => "$h2oHdir",
        timeout => 60,
        tries   => 3,
        #creates => "$h2oHdir/h2o-3.0.1.7.zip",
        #refreshonly => true,
        #notify => Exec['unzip h2o'],
        #before  => Exec["unzip h2o"],
    }
}

# source: http://stackoverflow.com/questions/11327582/puppet-recipe-installing-tarball
class h2o {
	exec { "mkdir_${h2oHdir}": command => "mkdir -p $h2oHdir" }
	exec { "wget_${h2oTarball}":
		command => "wget -nc $h2oTarball -P $h2oHdir/",
		#command => "wget -nc $h2oTarball",
		#cwd => "$h2oHdir",
		timeout => 60,
		tries   => 3,
		#creates => "$h2oHdir/h2o-3.0.1.7.zip",
		#refreshonly => true,
		#notify => Exec['unzip h2o'],
		before  => Exec["unzip h2o"],
	}
	exec { 'unzip h2o': 
		command => "unzip -o $h2oHdir/h2o-3.0.1.7.zip -d $h2oHdir/", 
		#command => "/usr/bin/unzip -o $h2oHdir/h2o-3.0.1.7.zip",
		#cwd => "$h2oHdir",
		timeout => 60, 
		tries   => 3,
		require => Class["unzip"],
	}
	#exec { 'run h2o':      command => "java -jar $h2oHdir/h2o-3.0.1.7/h2o.jar",      timeout => 5, tries   => 3 }
}

class sparkling-water {
	exec { "mkdir $sparklingWaterHdir": command => "mkdir -p $sparklingWaterHdir" }
	exec { "bashrc touch":
		command => "echo \"export SPARK_HOME='/home/qore/mldev/lib/ml/spark/spark-1.4.0-bin-hadoop2.4'\" >> /home/qore/.bashrc",
		before  => Exec["wget $sparklingWaterTarball"],
	}
	exec { "wget $sparklingWaterTarball":
		command => "wget -nc $sparklingWaterTarball -P $sparklingWaterHdir/",
		#command => "wget -nc $sparklingWaterTarball",
		#cwd => "$sparklingWaterHdir",
		timeout => 60,
		tries   => 3,
		#creates => "$sparklingWaterHdir/sparkling-water-1.4.3.zip",
		#refreshonly => true,
		#notify => Exec['unzip sparkling'],
		before  => Exec["unzip sparkling"],
	}
	exec { 'unzip sparkling': 
		command => "unzip -o $sparklingWaterHdir/sparkling-water-1.4.3.zip -d $sparklingWaterHdir/", 
		#command => "/usr/bin/unzip -o $sparklingWaterHdir/sparkling-water-1.4.3.zip",
		#cwd => "$sparklingWaterHdir",
		timeout => 60, 
		tries   => 3,
		require => Class["unzip"],
	}
	#exec { 'run sparkling':      command => "$sparklingWaterHdir/sparkling-water-1.4.3/bin/sparkling-shell",      timeout => 5, tries   => 3 }
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
		command => "tar zxf $sparkHdir/spark-1.4.0-bin-hadoop2.4.tgz -C $sparkHdir/", 
		timeout => 60, 
		tries   => 3,
		#require => File["$sparkHdir/spark-1.4.0-bin-hadoop2.4.tgz"],
	}
	#exec { 'run spark':      command => "$sparkHdir/spark-1.4.0-bin-hadoop2.4/bin/spark-shell",        timeout => 60, tries   => 3 }
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

#include apache

include system-update
include nfs-server
include nfs-client
include unzip
include curl
include javart
include h2o
include spark
include sparkling-water
include crontab
include nodejs
include cassandra
include xrdp
