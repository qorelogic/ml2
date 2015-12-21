
liquidInitialSetup() {
	adduser --home=/home/qore qore
	
	cd /home/qore/
	export HOME='/home/qore'
	
	ssh-keygen 
	#ssh -oStrictHostKeyChecking=no qore@104.236.64.84
	sudo -u qore ssh-keygen
	rsync -avP --partial qore@104.236.64.84:/home/qore/.ssh/id_rsa /home/qore/.ssh/id_rsa
	rsync -avP --partial qore@104.236.64.84:/home/qore/.ssh/id_rsa.pub /home/qore/.ssh/id_rsa.pub
	
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

setupAliases() {
	echo 'qore    ALL=(ALL:ALL) ALL' >> /etc/sudoers
	echo '. /mldev/etc/aliases.sh' >> /home/qore/.bashrc
	echo '. /mldev/etc/aliases.sh' >> /root/.bashrc
	echo "alias p='. /mldev/etc/aliases.sh'" >> /home/qore/.bashrc
	echo "alias p='. /mldev/etc/aliases.sh'" >> /root/.bashrc
	. ~/.bashrc
}

liquidInitialSetup
setupAliases
