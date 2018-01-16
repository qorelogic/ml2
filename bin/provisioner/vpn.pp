
Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

class vpn-server {
    package { "pptpd":
    ensure  => present,
    require => Class["system-update"],
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
    exec { "pptpd.conf localip":
    	command => "sudo perl -pi -we 's/^(#)?logwtmp (.*)/#logwtmp/g' /etc/pptpd.conf",
       #before  => Exec["pptpd.conf remoteip"],
    }
    exec { "chap-secrets":
    	command => "sudo perl -pi -we 's/^box1 (.*)/box1 pptpd qweqwe */g' /etc/ppp/chap-secrets",
        before  => Exec["ms-dns"],
    }
    exec { "": command => "sudo perl -pi -e 's/.*(logwtmp.*)/#\1/g' /etc/ppp/pptpd-options", before  => Exec["p1"] }
    exec { "ms-dns":
    	command => "sudo perl -pi -we 's/.*ms-dns (.*)//g' /etc/ppp/pptpd-options",
        before  => Exec["p1"],
    }
    exec { "p1": before => Exec["p2"],            command => "echo 'ms-dns 8.8.8.8' >> /etc/ppp/pptpd-options"}
    exec { "p2": before => Exec["pptpd restart"], command => "echo 'ms-dns 8.8.4.4' >> /etc/ppp/pptpd-options"}
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

#    exec { "p1": before => Exec["p2"], command => "perl -pi -e 's/.*(localip).*//g' /etc/pptpd.conf"}
#    exec { "p2": before => Exec["p3"], command => "echo 'localip 10.0.0.1' >> /etc/pptpd.conf"}

#    exec { "p3": before => Exec["p4"], command => "perl -pi -e 's/.*(remoteip).*//g' /etc/pptpd.conf"}
#    exec { "p4": before => Exec["p5"], command => "echo 'remoteip 10.0.0.100-200' >> /etc/pptpd.conf"}

#    exec { "p5": before => Exec["p6"], command => "echo 'ms-dns 8.8.8.8' >> /etc/pptpd.conf"}

#    exec { "p6": before => Exec["p7"], command => "perl -pi -e 's/.*(box1 ).*//g' /etc/chap-secrets" }
#    exec { "p7": before => Exec["p8"], command => "echo 'box1 pptpd qweqwe1' >> /etc/chap-secrets"}

#    exec { "p8": before => Exec["p9"],  command => "perl -pi -e 's/.*(ms-dns ).*//g' /etc/ppp/pptpd-options"}
#    exec { "p9": before => Exec["p10"], command => "echo 'ms-dns 8.8.8.8' >> /etc/ppp/pptpd-options"}
#    exec { "p10": before => Exec["p11"],   command => "echo 'ms-dns 8.8.4.4' >> /etc/ppp/pptpd-options" }

#    exec { "p11": before => Exec["p12"],   command => "service pptpd restart" }

#    exec { "p12": before => Exec["p13"],   command => "perl -pi -e 's/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/g' "}
#    exec { "p13": before => Exec["p14"],   command => "sysctl -p"}
#    exec { "p14": before => Exec["   "],   command => "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE && iptables-save"}

#perl -pi -e 's/.*(localip).*/\1 10.0.0.1/g' /etc/pptpd.conf
#perl -pi -e 's/.*(remoteip).*/\1 10.0.0.100-200/g' /etc/pptpd.conf
#echo 'box1 pptpd qweqwe1' >> /etc/chap-secrets

#perl -pi -e 's/#(ms-dns ).*/\1 8.8.8.8/g' /etc/pptpd.conf
#perl -pi -e 's/#(ms-dns ).*/\1 8.8.4.4/g' /etc/pptpd.conf

}

import 'system-update.pp'
include vpn-server
