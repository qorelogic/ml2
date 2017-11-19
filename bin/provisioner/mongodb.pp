
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

class mongodb {

# source: http://stackoverflow.com/questions/1139127/how-to-trust-a-apt-repository-debian-apt-get-update-error-public-key-is-not-av
#apt-get install debian-keyring
#gpg --keyserver pgp.mit.edu --recv-keys 9ECBEC467F0CEB10
#gpg --armor --export 9ECBEC467F0CEB10 | apt-key add -
    exec { "reconfigure":
	command => "sudo dpkg-reconfigure -phigh -a",
        timeout => 60,
        tries   => 3,
        before  => Exec["mongo purge"],
	returns => [0, 1],
    }
    exec { "mongo purge":
	command => "sudo /usr/binapt-get purge -y mongodb-org",
	#command => "sudo /usr/bin/apt-get purge -y mongodb-server",
        timeout => 60,
        tries   => 3,
        before  => Exec["mongo autoremove"],
	returns => [0, 1],
    }
    exec { "mongo autoremove":
	command => "sudo /usr/bin/apt-get autoremove -y",
        timeout => 60,
        tries   => 3,
        before  => Exec["mongo rm mongodb.list"],
    }
    exec { "mongo rm mongodb.list":
	command => "rm /etc/apt/sources.list.d/mongodb.list 2>&1 > /dev/null",
        timeout => 60,
        tries   => 3,
        before  => Exec["mongo add deb sources"],
	returns => [0, 1],
    }
    exec { "mongo add deb sources":
	command => "echo 'deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.0 main' | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list",
        timeout => 60,
        tries   => 3,
        before  => Exec["mongo aptget update"],
    }
    exec { "mongo aptget update":
	command => "sudo apt-get update",
        timeout => 60,
        tries   => 3,
        before  => Exec["mongo aptget install"],
   }
    exec { "mongo aptget install":
	command => "sudo apt-get install -y --force-yes mongodb-org",
	#command => "sudo apt-get install -y --force-yes mongodb-server",
        timeout => 6000,
        tries   => 3,        
        before  => Exec["exportlocale"],
    }
    exec { "exportlocale":
	command => "echo 'export LC_ALL=C' >> /root/.bashrc; echo 'export LC_ALL=C' >> /home/qore/.bashrc",
        timeout => 60,
        tries   => 3,        
    }
}

import 'system-update.pp'
include mongodb

