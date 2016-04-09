
class tty-js {
    exec { 'npm install tty.js': 
        command => "/usr/bin/npm install tty.js", 
        timeout => 300, 
        tries   => 3,
        #require => Class["nodejs"],
        #before  => Exec["rm node symlinks"],
    }


}

#import 'system-update.pp'
include tty-js
