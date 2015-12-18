su qore
cat ~/.bash_history
adduser --home=/home/qore qore
ssh-keygen 
#ssh -oStrictHostKeyChecking=no qore@104.236.64.84
#rsync -avP --partial qore@104.236.64.84:/home/qore/.ssh/id_rsa /home/qore/.ssh/id_rsa
sudo -u qore ssh-keygen
rsync -avP --partial qore@104.236.64.84:/home/qore/.ssh/id_rsa /home/qore/.ssh/id_rsa
rsync -avP --partial qore@104.236.64.84:/home/qore/.ssh/id_rsa.pub /home/qore/.ssh/id_rsa.pub
sudo -u qore git clone git@github.com:qorelogic/ml2.git /home/qore/mldev
#cat /home/qore/.ssh/id_rsa.pub 
cd /home/qore/
sudo -u qore git clone git@github.com:qorelogic/ml2.git /home/qore/mldev
ln -s /home/qore/mldev /mldev
apt-get update
apt-get install puppet
apt-get install -y puppet
ls
cd /mldev/bin
sudo -u qore git fetch origin forecaster.refactored-0.3:forecaster.refactored-0.3
sudo -u qore git checkout forecaster.refactored-0.3
sudo -u qore git pull origin forecaster.refactored-0.3
#nano provisioner/default.pp 
#puppet apply provisioner/default.pp 
nano provisioner/default.pp 
puppet apply provisioner/default.pp

