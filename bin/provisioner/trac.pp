
import 'system-update.pp'

$hdir        = "/mldev"
$installHdir = "$hdir/lib/ml"

### Trac ######################################################################
# source: https://trac.edgewall.org/wiki/TracDownload
$tracV           = "Trac-1.0.10"
$tracTarball     = "$tracV.tar.gz"
$tracTarballURL  = "http://download.edgewall.org/trac/$tracTarball"
$tracHdir        = "$installHdir/task-tracking/trac"

class trac {
    # install pip
    package { "libsqlite3-dev": ensure  => present, require => Class["system-update"], before  => Exec["pip install pysqlite"] }
    exec { "pip install pysqlite": command => "/usr/local/bin/pip install pysqlite==2.8.1", before  => Exec["mkdir -p $tracHdir"] }
    exec { "pip install Genshi":   command => "/usr/local/bin/pip install Genshi==0.7",     before  => Exec["mkdir -p $tracHdir"] }
    exec { "pip install trac":     command => "/usr/local/bin/pip install trac",            before  => Exec["mkdir -p $tracHdir"] }
    exec { "mkdir -p $tracHdir":   command => "/bin/mkdir -p $tracHdir",                    before  => Exec["wget -nc $tracTarball"] }
    exec { "chown $tracHdir":   command => "/bin/chown -R qore: $tracHdir",                 before  => Exec["wget -nc $tracTarball"] }
    exec { "wget -nc $tracTarball":
        command => "/usr/bin/wget -nc $tracTarballURL -P $tracHdir/",
        timeout => 60,
        tries   => 3,
        before  => Exec["untar trac"],
    }
    exec { 'untar trac': 
        command => "/bin/tar zxf $tracHdir/$tracTarball -C $tracHdir/", 
        timeout => 60, 
        tries   => 3,
        #require => File["$tracHdir/$tracTarball"],
        #before  => Exec["rm trac symlinks"],
    }
    #exec { 'rm trac symlinks':
    #	command => "rm -f /usr/bin/trac; rm -f /usr/bin/npm;", 
    #	timeout => 60, 
    #	tries   => 3,
    #	before  => Exec["trac symlinks"],
    #}
    #exec { 'trac symlinks':
    #	command => "ln -s $tracHdir/$tracV/bin/trac /usr/bin/trac; ln -s $tracHdir/$tracV/bin/npm /usr/bin/npm;",
    #	timeout => 60, 
    #	tries   => 3,
    #}
    #exec { 'run trac':      command => "$tracHdir/bin/trac",        timeout => 60, tries   => 3 }
}

include trac
