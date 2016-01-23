
class system-update {
  exec { 'apt-get update':
    command => '/usr/bin/apt-get update',
  }

  $sysPackages = [ "build-essential", "htop", 'iotop', 'python-pip', 'python-dev' ]
  package { $sysPackages:
    ensure => "installed",
    require => Exec['apt-get update'],
  }
}

include system-update

