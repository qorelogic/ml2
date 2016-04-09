
#echo "DEBUG: I am .bashrc"

#python /mldev/assets/users/foo/test.py

touch /tmp/qore.dev.log
dpwd="`pwd`"
cd /mldev/bin/datafeeds
python /mldev/bin/datafeeds/oanda.py feed
cd $dpwd

sleep 10000
exit

echo "DEBUG: I am .bash_login"
