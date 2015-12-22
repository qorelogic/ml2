
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

class vpn-server {
    package { "pptpd":
    ensure  => present,
    #require => Class["system-update"],
    
    }
    #$qwe = generate("/bin/echo", "-n", "Hallo Welt")
    # source: https://groups.google.com/forum/#!topic/puppet-users/HXE4w_TlulM
    # source: http://stackoverflow.com/questions/5171901/sed-command-find-and-replace-in-file-and-overwrite-file-doesnt-work-it-empties
    $localip = inline_template("<%= %x{ ifconfig | grep -i 'inet ' | grep -v '127.0.0.' | perl -pe 's/[\s]+/ /g' | cut -d' ' -f3 | cut -d':' -f2  | perl -pe 's/\n//g' } %>")
    $miface = inline_template("<%= %x{ route -n | grep -i '0.0.0.0' | grep 'U ' | perl -pe 's/[\s]+/ /g' | cut -d' ' -f8  | perl -pe 's/\n//g' } %>")
    $qaz = inline_template("<%= %x{ echo 'box1 pptpd passwd *' >> /etc/ppp/chap-secrets } %>")
    #$qwe  = generate("/bin/echo", "-n", "$mvar")
    exec { "pptpd.conf localip":
    	command => "sudo perl -pi -we 's/^(#)?localip (.*)/localip $localip/g' /etc/pptpd.conf",
        before  => Exec["pptpd.conf remoteip"],
    }
    exec { "pptpd.conf remoteip":
    	command => "sudo perl -pi -we 's/^(#)?remoteip (.*)/remoteip 192.168.0.234-238,192.168.0.245/g' /etc/pptpd.conf",
        before  => Exec["chap-secrets"],
    }
    exec { "chap-secrets":
    	command => "sudo perl -pi -we 's/^box1 (.*)/box1 pptpd qweqwe */g' /etc/ppp/chap-secrets",
        before  => Exec["ms-dns"],
    }
    exec { "ms-dns":
    	command => "sudo perl -pi -we 's/^ms-dns (.*)/ms-dns 8.8.8.8/g' /etc/ppp/pptpd-options",
        before  => Exec["pptpd restart"],
    }
    exec { "pptpd restart":
    	command => "service pptpd restart",
        before  => Exec["forwarding"],
    }
    exec { "forwarding":
    	command => "sudo perl -pi -we 's/^(#)?(net.ipv4.ip_forward)[\s]*=[\s]{0,1}(.+)/\2 = 1\n/g' /etc/sysctl.conf",
        before  => Exec["sysctl -p"],
    }
    exec { "sysctl -p":
    	command => "sudo sysctl -p",
        before  => Exec["masquerade"],
    }
    exec { "masquerade":
    #	command => "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE && iptables-save",
    #	command => "iptables -t nat -A POSTROUTING -o venet0:0 -j MASQUERADE && iptables-save",
    	command => "iptables -t nat -A POSTROUTING -o $miface -j MASQUERADE && iptables-save",
    }
}

import 'system-update.pp'
include vpn-server
