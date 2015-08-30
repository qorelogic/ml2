
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

$hdir        = "/mldev"
$installHdir = "$hdir/lib/ml"
$h2oHdir     = "$installHdir/h2o"
$sparkHdir   = "$installHdir/spark"

$h2oTarball   = "http://h2o-release.s3.amazonaws.com/h2o/rel-simons/7/h2o-3.0.1.7.zip"
$sparkTarball = "http://d3kbcqa49mib13.cloudfront.net/spark-1.4.0-bin-hadoop2.4.tgz"

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
	#exec { 'run h2o':      command => "java -jar $sparkHdir/spark-1.4.0-bin-hadoop2.4/bin/...",        timeout => 60, tries   => 3 }
}

#include apache

include system-update
include unzip
include javart
include h2o
include spark
