
class tty-js {
    exec { 'npm install tty.js': 
        command => "/usr/bin/npm install tty.js", 
        timeout => 300, 
        tries   => 3,
        #require => Class["nodejs"],
        #before  => Exec["rm node symlinks"],
    }
    exec { 'useradd foo': 
        command => "useradd -m -d /mldev/assets/users/foo foo", 
        timeout => 30,
        tries   => 3,
        #require => Class["nodejs"],
        #before  => Exec["rm node symlinks"],
    }
    exec { 'edit passwd foo':
        command => "useradd -m -p qwqw -d /mldev/assets/users/foo foo",
        timeout => 30,
        tries   => 3,
        #require => Class["nodejs"],
        #before  => Exec["rm node symlinks"],
    }
}

#import 'system-update.pp'
include tty-js
