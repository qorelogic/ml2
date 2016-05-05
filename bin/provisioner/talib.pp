
#Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

### Ta-Lib ####################################################################
$nodeVe          = "v4.1.0"
$nodeV           = "node-$nodeVe-linux-x64"
$nodeTarball     = "$nodeV.tar.gz"
$nodeTarballURL  = "https://nodejs.org/dist/$nodeVe/$nodeTarball"
#$nodeTarballURL  = "https://nodejs.org/dist/latest/$nodeTarball"
$nodeHdir        = "$installHdir/node"

class talib {
	exec { "mkdir_talib": 
		command => "/bin/mkdir -p /mldev/lib/hft/talib/",
		before  => Exec["wget_talib"],
     }

	exec { "wget_talib":
		command => "/usr/bin/wget -nc http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -P /mldev/lib/hft/talib/",
		timeout => 60,
		tries   => 3,
		before  => Exec["untar_talib"],
	}

	exec { 'untar_talib':
		command => "/bin/tar zxf /mldev/lib/hft/talib/ta-lib-0.4.0-src.tar.gz -C /mldev/lib/hft/talib/",
		timeout => 60, 
		tries   => 3,
		before  => Exec["makedistclean_talib"],
	}

     exec { 'makedistclean_talib':
        command => '/usr/bin/make distclean', 
        cwd     => '/mldev/lib/hft/talib/ta-lib/',
        before  => Exec["configure_talib"],
        returns => [0, 2],
     } 

     exec { 'configure_talib':
        command => '/mldev/lib/hft/talib/ta-lib/configure', 
        cwd     => '/mldev/lib/hft/talib/ta-lib/',
        before  => Exec["make_talib"],
     } 

     exec { 'make_talib':
        command => '/usr/bin/make', 
        cwd     => '/mldev/lib/hft/talib/ta-lib/',
        before  => Exec["makeinstall_talib"],
     } 

     exec { 'makeinstall_talib':
        command => '/usr/bin/make install',
        cwd     => '/mldev/lib/hft/talib/ta-lib/',
        before  => Exec["symlinks_talib"],
     } 

	#exec { "gitclone_openflights":
	#	command => "git clone https://github.com/jpatokal/openflights.git /mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git",
	#	timeout => 60,
	#	tries   => 3,
	#	#refreshonly => true,
	#	before  => Exec["unzip openflights"],
	#}
	#exec { 'unzip openflights': 
	#	command => "unzip -o /mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git/data/DAFIFT_0610_ed6.zip -d /mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git/data/DAFIFT_0610_ed6", 
	#	timeout => 60, 
	#	tries   => 3,
	#	require => Class["unzip"],
	#}

#	exec { "mkdir -p $nodeHdir": command => "/bin/mkdir -p $nodeHdir" }
#	exec { "wget -nc $nodeTarball":
#		command => "/usr/bin/wget -nc $nodeTarballURL -P $nodeHdir/",
#		timeout => 60,
#		tries   => 3,
#		before  => Exec["untar node"],
#	}
#	exec { 'untar node': 
#		command => "/bin/tar zxf $nodeHdir/$nodeTarball -C $nodeHdir/", 
#		timeout => 60, 
#		tries   => 3,
#		#require => File["$nodeHdir/$nodeTarball"],
#		before  => Exec["rm node symlinks"],
#	}
#	#exec { 'run node':      command => "$nodeHdir/bin/node",        timeout => 60, tries   => 3 }

#	exec { 'rm node symlinks':
#		command => "/bin/rm -f /usr/bin/node; rm -f /usr/bin/npm;", 
#		timeout => 60, 
#		tries   => 3,
#		before  => Exec["node symlinks"],
#	}

	exec { 'symlinks_talib':
		command => "/bin/ln -s /usr/local/lib/libta_lib.so.0 /usr/lib/libta_lib.so.0",
		timeout => 60, 
		tries   => 3,
           before  => Exec["pip install Ta-Lib"],
	}

      exec { "pip install Ta-Lib": command => "/usr/local/bin/pip install Ta-Lib", timeout => 60, tries => 3 }
}


include talib
