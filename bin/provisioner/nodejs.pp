
#Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

### NodeJS ####################################################################
$nodeVe          = "v4.1.0"
$nodeV           = "node-$nodeVe-linux-x64"
$nodeTarball     = "$nodeV.tar.gz"
$nodeTarballURL  = "https://nodejs.org/dist/$nodeVe/$nodeTarball"
#$nodeTarballURL  = "https://nodejs.org/dist/latest/$nodeTarball"
$nodeHdir        = "$installHdir/node"

class nodejs {
	exec { "mkdir -p $nodeHdir": command => "/bin/mkdir -p $nodeHdir" }
	exec { "wget -nc $nodeTarball":
		command => "/usr/bin/wget -nc $nodeTarballURL -P $nodeHdir/",
		timeout => 60,
		tries   => 3,
		before  => Exec["untar node"],
	}
	exec { 'untar node': 
		command => "/bin/tar zxf $nodeHdir/$nodeTarball -C $nodeHdir/", 
		timeout => 60, 
		tries   => 3,
		#require => File["$nodeHdir/$nodeTarball"],
		before  => Exec["rm node symlinks"],
	}
	exec { 'rm node symlinks':
		command => "/bin/rm -f /usr/bin/node; rm -f /usr/bin/npm;", 
		timeout => 60, 
		tries   => 3,
		before  => Exec["node symlinks"],
	}
	exec { 'node symlinks':
		command => "/bin/ln -s $nodeHdir/$nodeV/bin/node /usr/bin/node; ln -s $nodeHdir/$nodeV/bin/npm /usr/bin/npm;",
		timeout => 60, 
		tries   => 3,
	}
	#exec { 'run node':      command => "$nodeHdir/bin/node",        timeout => 60, tries   => 3 }
}

include nodejs

