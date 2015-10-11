
class nfs-server {
    package { "nfs-kernel-server":
    ensure  => present,
    require => Class["system-update"],
    }
    exec { "etc exports":
        command => "/bin/grep -v '/mldev/bin/data' /etc/exports | grep -v '/var/lib/mongodb' | grep -v '/mldev/lib/DataPipeline' | /usr/bin/tee /etc/exports > /dev/null",
        timeout => 60,
        tries   => 3,
        #notify => Exec['unzip h2o'],
        before  => Exec["add2exports"],
    }
    exec { "add2exports":
        command => "/bin/echo '/mldev/bin/data  *.*.*.*(rw,sync,anonuid=1000,anongid=1000,all_squash)' >> /etc/exports",
        timeout => 60,
        tries   => 3,
        before  => Exec["add2exports2"],
    }
    exec { "add2exports2":
        command => "/bin/echo '/var/lib/mongodb  *.*.*.*(rw,sync,anonuid=1000,anongid=1000,all_squash)' >> /etc/exports",
        timeout => 60,
        tries   => 3,
        before  => Exec["add2exports3"],
    }
    exec { "add2exports3":
        command => "/bin/echo '/mldev/lib/DataPipeline  *.*.*.*(rw,sync,anonuid=1000,anongid=1000,all_squash)' >> /etc/exports",
        timeout => 60,
        tries   => 3,
        before  => Exec["nfs-kernel-server restart"],
    }
    exec { "nfs-kernel-server restart":
        command => "/usr/bin/service nfs-kernel-server restart",
        #command => "exportfs -a",
        timeout => 60,
        tries   => 3,
    }
}

import 'system-update.pp'
include nfs-server

