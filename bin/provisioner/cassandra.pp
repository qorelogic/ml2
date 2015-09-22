
#import 'systemupdate.pp'

# source: http://docs.datastax.com/en/cassandra/2.1/cassandra/install/installDeb_t.html
class cassandra {
        exec {
                "AddDataStaxCommunityRepository2cassandra.sources.list":
                command => "/bin/echo 'deb http://debian.datastax.com/community stable main' | /usr/bin/tee -a /etc/apt/sources.list.d/cassandra.sources.list",
                before  => Exec["AddDataStaxReposKey2aptitudeTrustedKeys"]
        }
        exec {
                "AddDataStaxReposKey2aptitudeTrustedKeys":
                command => '/usr/bin/curl -L http://debian.datastax.com/debian/repo_key | /usr/bin/apt-key add -',
                before  => Exec["InstallCassandra"]
        }
        $xv = '9'
        exec {
                "InstallCassandra":
                command => "/usr/bin/apt-get install -y --force-yes dsc21=2.1.${xv}-1 cassandra=2.1.${xv}",
                before  => Exec["InstallCassandraTools"],
                require => Class["system-update"]
        }
        exec {
                ## Optional utilities
                "InstallCassandraTools":
                command => "/usr/bin/apt-get install cassandra-tools=2.1.${xv}",
                require => Class["system-update"]
        }
}

include system-update
include cassandra
