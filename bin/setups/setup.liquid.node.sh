#!/bin/sh


# NOTE: This is an example that sets up SSH authorization.  To use it, you'd need to replace "ssh-rsa AA... youremail@example.com" with your SSH public.
# You can replace this entire script with anything you'd like, there is no need to keep it


#mkdir -p /root/.ssh
#chmod 600 /root/.ssh
#echo ssh-rsa AA... youremail@example.com > /root/.ssh/authorized_keys
#chmod 700 /root/.ssh/authorized_keys

liquidInitialSetup() {
        adduser --home=/home/qore qore
        
        ipaddr="104.207.135.67"
        cd /home/qore/
        export HOME='/home/qore'
        
	echo '-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEA6KTgumtTekyT2DY1nUHjVzvlrKJ+TGE7f7ky9R8J/o85crfV
K7Nf33sNubdWrZuGPvIRL/uFeCxaeC14dqlk3cnUPKiHB5/B3/xY79y3P4LPR/Q/
OB9Im5nMEynKce+S0WatKMA4lneIVeM4JjQtCzy1GqmwWqEjwjXIP9NjMBWDXrtw
M16u0am5E/YS+U5yxoUctLvBZYd6D8rmv2wPSM5PS5vDaCC4wzCuzUJMoT65FiVi
Sxz5vKGPBCpzAjeiuAEZbaxeVTxjaNVIgoxlDyB6ily+3kXfjwBIBUrkUSPjBpc9
yjYUibtm3C5DNjSL+7xXO7/HuFxc0MStCXfUUQIDAQABAoIBAQCM1AIV1xJZXjHB
GE+sOk5caC3IKzU5F0LlNj7ak0eBiUHFZ/Lq2VKX/e15FrqprRO+1toAqclJzc+W
IDBj5Hbiq2KGtZ3Hx7Wc2S0dRgbHs2+2puv+FTHmv1sB3rJl9hhyGi2IFZQrwYAO
PdWnir4Zp04aLc5LjnAPCG+H83Z/i96qpju5+tyUtCIJGIaQ6j5Zus3/aobfQ6Qa
+/XdauC3i8DJSrvkyYLFONq/JdLuxjVuFgCq7C7SEwgoIZU/+UBm/CC8v+cGCKv4
+rNfbvaZc6gWi4qvwa7rNbCUdvFxV2JpPs8LRIZ2b56RhCrBF/O0fzCHTQqH2cEp
tab44oYBAoGBAP0NvdUEJq0z2jpZiPMqj7A0Oor+xUs9rmvzpB9dMaPkaVSbPVa8
Tzlv/tYZeti+DhPL6ZDgC5tsIxs5Pd8CSr6g66IEZH0Ahdj76hF10AWnUeQ2fWj7
HMN/qeCTBFIIztXuy9gqniM+692iH8tQogU+EfhmiDWZ90g6WbAoTGOZAoGBAOta
TYeQ82iBJ60AJyAOcW7dSuF0WJvHCbbS5ceU0HLp3Q2M7rrU+pel0ftx2jrq0qoC
+KoGD7SJXvKcWUMYjzE2wFdmLeOq0pxhNXkP6+D6MjXUVuMbgUpwDMPJXgWbcL+n
ZxdMJbBh80dZHbima2qhDCoIL1nRWF/iNWX+e2l5AoGBAMO51zRlq4yX6JjtG7IJ
H25IV2eeuvcBVGGG51CjAnwjdRzNndnyeMySRWdP+eaeycCiHZvCzvd94oFx+tr8
qNddHCQKhbbxqpUz881hdG6LBhof00xZvduwaLKcw+C3k1OBCgW+oOXeCw04EqNt
UIQBiGC63WuoFM225BwOb1cxAoGBAOYhl9vupcRTPkuQ8bELzmk8o6LPFHHGbz5A
/IRqhGVJPmionSs9ZIfykeAP1Pd1dGbfnu0KHkNHa/tJXJMaKbJSukL72/VZrLVS
7GmjYt/LZltydT9/Pq5d4G11sqVC+D2/YDPMtrHBJZRnlINg33oVXgKfnEV0SbkA
RXylGWHpAoGBAIgSI7AuIpLhbw1mTCUTkxNRdVLS2NjsJUon9mguW9qGx0F5VOzz
6ak4Bdwon/HXDETpGbL+tJNnildSrJ9GL2Mwn2xSCLY/18BKHghLw8B/iZ4AnJbU
Xw/xa8PCZQlcQni0YF+7vOyIU/9PJ+NV91eAOFbnycVXiVv3X1U2uJN8
-----END RSA PRIVATE KEY-----' > /home/qore/.ssh/id_rsa
	chown qore: /home/qore/.ssh/id_rsa
	chmod 0600 /home/qore/.ssh/id_rsa

	echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDopOC6a1N6TJPYNjWdQeNXO+Wson5MYTt/uTL1Hwn+jzlyt9Urs1/few25t1atm4Y+8hEv+4V4LFp4LXh2qWTdydQ8qIcHn8Hf/Fjv3Lc/gs9H9D84H0ibmcwTKcpx75LRZq0owDiWd4hV4zgmNC0LPLUaqbBaoSPCNcg/02MwFYNeu3AzXq7RqbkT9hL5TnLGhRy0u8Flh3oPyua/bA9Izk9Lm8NoILjDMK7NQkyhPrkWJWJLHPm8oY8EKnMCN6K4ARltrF5VPGNo1UiCjGUPIHqKXL7eRd+PAEgFSuRRI+MGlz3KNhSJu2bcLkM2NIv7vFc7v8e4XFzQxK0Jd9RR qore@vultr.guest' > /home/qore/.ssh/id_rsa.pub
	chown qore: /home/qore/.ssh/id_rsa.pub
	chmod 0644 /home/qore/.ssh/id_rsa.pub

        #ssh-keygen -N '' -f /root/.ssh/id_rsa
	echo -e  'y\n'|ssh-keygen -q -t rsa -N "" -f /root/.ssh/id_rsa
        #ssh -oStrictHostKeyChecking=no qore@$ipaddr
        #sudo -u qore ssh-keygen -N '' -f /home/qore/.ssh/id_rsa
	echo -e  'y\n' | sudo -u qore ssh-keygen -q -t rsa -N "" -f /home/qore/.ssh/id_rsa
#        rsync -avP  -e 'ssh -oStrictHostKeyChecking=no' --partial qore@$ipaddr:/home/qore/.ssh/id_rsa /home/qore/.ssh/id_rsa
#        rsync -avP  -e 'ssh -oStrictHostKeyChecking=no' --partial qore@$ipaddr:/home/qore/.ssh/id_rsa.pub /home/qore/.ssh/id_rsa.pub
        
	# source: http://debuggable.com/posts/disable-strict-host-checking-for-git-clone:49896ff3-0ac0-4263-9703-1eae4834cda3
	echo "Host github.com\n\tStrictHostKeyChecking no\n" > /root/.ssh/config
	echo "Host github.com\n\tStrictHostKeyChecking no\n" > /home/qore/.ssh/config
	chown qore: /home/qore/.ssh/config
        sudo -u qore git clone git@github.com:qorelogic/ml2.git /home/qore/mldev
        ln -s /home/qore/mldev /mldev
        ln -s /home/qore/mldev /ml.dev
        cd /mldev/bin
        
        apt-get update
        apt-get install -y puppet
        
        sudo -u qore git fetch origin forecaster.refactored-0.3:forecaster.refactored-0.3
        sudo -u qore git checkout forecaster.refactored-0.3
        sudo -u qore git pull origin forecaster.refactored-0.3
        
        #nano provisioner/default.pp 
        puppet apply provisioner/default.pp
}

setupAlias() {

        if [ "$1" == "" ]; then
                print "usage: <>"
		return 0
        else
        muser="$1"

        if [ "$muser" == "root" ]; then
                muserHdir="/root"
        else
                muserHdir="/home/$muser"
        fi

        #echo ''
        #echo 'Added by set.liquid.node.sh''
        echo "$muser    ALL=(ALL:ALL) ALL" >> /etc/sudoers
        echo ". /mldev/etc/aliases.sh" >> $muserHdir/.bashrc
        echo "alias qp='. /mldev/etc/aliases.sh'" >> $muserHdir/.bashrc
        fi
}

setupAliases() {

        setupAlias root 2> /dev/null
        setupAlias qore 2> /dev/null
        setupAlias qore2 2> /dev/null

        . ~/.bashrc
}

#liquidInitialSetup
setupAliases
