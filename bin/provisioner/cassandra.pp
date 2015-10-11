
# source: http://docs.datastax.com/en/cassandra/2.1/cassandra/install/installDeb_t.html
# source: http://stackoverflow.com/questions/1139127/how-to-trust-a-apt-repository-debian-apt-get-update-error-public-key-is-not-av
#apt-get install debian-keyring
#gpg --keyserver pgp.mit.edu --recv-keys 350200F2B999A372
#gpg --armor --export 350200F2B999A372 | apt-key add -
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

import 'system-update.pp'
include cassandra

