
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

class redis {

#$ wget http://download.redis.io/releases/redis-4.0.2.tar.gz
#$ tar xzf redis-4.0.2.tar.gz
#$ cd redis-4.0.2
#$ make

    exec { "wget redis":
	command => "wget -nc --no-check-certificate http://download.redis.io/releases/redis-4.0.2.tar.gz -P /opt/",
        timeout => 6000,
        tries   => 3,
        before  => Exec["untar redis"],
	returns => [0, 1],
    }
    exec { "untar redis":
	command => "tar zxf /opt/redis-4.0.2.tar.gz -C /opt/",
        timeout => 600,
        tries   => 3,
        before  => Exec["make redis"],
	returns => [0, 1],
    }
    exec { "make redis":
	command => "make -C /opt/redis-4.0.2/",
        timeout => 6000,
        tries   => 3,
        #before  => Exec[""],
	returns => [0, 1],
    }
}
import 'system-update.pp'
include redis

