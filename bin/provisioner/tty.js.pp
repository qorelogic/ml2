
class tty-js {
    exec { 'npm install tty.js': 
        command => "/usr/bin/npm install tty.js", 
        timeout => 300, 
        tries   => 3,
        #require => Class["nodejs"],
        before  => Exec["useradd foo"],
    }

    exec { 'useradd foo': 
        command => "/usr/sbin/useradd -m --password qwqw --shell /bin/bash -d /mldev/assets/users/foo foo", 
        timeout => 30,
        tries   => 3,
        before  => Exec["add .bashrc hook"],
    }

    # http://www.linuxquestions.org/questions/linux-general-1/ubuntu-how-to-run-python-script-on-login-352191/
    # http://askubuntu.com/questions/98433/run-a-script-on-login-using-bash-login
    exec { 'add .bashrc hook': 
        command => "/bin/echo 'bash.startup.sh' >> /mldev/assets/users/foo/.bashrc", 
        timeout => 30,
        tries   => 3,
#        before  => Exec["edit passwd foo"],
    }

    # foo:x:1001:1001::/mldev/assets/users/foo:/bin/bash
    # cat /etc/passwd | perl -pe 's/^foo:x:(.*?):(.*?):(.*?):(.*?):(.*?)/foo:x:\1:\2:\3:\/mldev\/assets\/users\/foo:\5/g'
#    exec { 'edit passwd foo':
#        command => "",
#        timeout => 30,
#        tries   => 3,
#        #before  => Exec["rm node symlinks"],
#    }
}

#import 'system-update.pp'
include tty-js
