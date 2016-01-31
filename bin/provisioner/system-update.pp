
class system-update {
  exec { 'apt-get update':
    command => '/usr/bin/apt-get update',
  }

  # sudo apt-get install python-scipy
  # python packages for datafeeds: python-matplotlib
  $sysPackages = [ "build-essential", "htop", 'iotop', 'python-pip', 'python-dev',  "python-scipy", 'ipython', 'ipython-notebook', 'python-matplotlib', 'python-tk', 'python-pil' ]
  package { $sysPackages:
    ensure => "installed",
    require => Exec['apt-get update'],
  }
}

include system-update

