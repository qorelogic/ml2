
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

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
	exec { 'wget http://h2o-release.s3.amazonaws.com/h2o/rel-simons/7/h2o-3.0.1.7.zip':
	  command => 'wget http://h2o-release.s3.amazonaws.com/h2o/rel-simons/7/h2o-3.0.1.7.zip -P /home/qore/',
	  timeout => 60,
	  tries   => 3
	}
	exec { 'unzipping h2o': command => 'unzip /home/qore/h2o-3.0.1.7.zip -d /home/qore/', timeout => 60, tries   => 3 }
	exec { 'run h2o':       command => 'java -jar /home/qore/h2o-3.0.1.7/h2o.jar',     timeout => 5, tries   => 3 }
}


#include apache
include system-update
include javart
include unzip
include h2o
