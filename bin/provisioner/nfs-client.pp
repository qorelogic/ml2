
class nfs-client {
    package { "nfs-common":
    ensure  => present,
    require => Class["system-update"],
    }
    #exec { "mkdir_nfs_share":
    #    command => "mkdir /mnt/nfs-share 2> /dev/null",
    #    #cwd => "$h2oHdir",
    #    timeout => 60,
    #    tries   => 3,
    #    #creates => "$h2oHdir/h2o-3.0.1.7.zip",
    #    #refreshonly => true,
    #    #notify => Exec['unzip h2o'],
    #    #before  => Exec["unzip h2o"],
    #}
}

import 'system-update.pp'
include nfs-client


