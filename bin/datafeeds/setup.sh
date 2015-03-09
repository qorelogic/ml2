MPWD=`pwd`

mlocal=~/.tmuxifier
mldir=/ml.dev

mdependencies() {
	sleep 1
	echo ''
	echo -n 'Need to install tmuxifier..  '
	sleep 3
	echo ' ..installing..'
	echo ''
	sleep 3
	git clone https://github.com/jimeh/tmuxifier.git $mlocal

	echo ''
	echo 'dependencies complete.'

}

minstall() {
	sleep 1
	#if [ -f $MPWD/tmuxifier/layouts/datafeeds.window.sh ]; then
	if [ ! -f $mlocal/layouts/datafeeds.window.sh ]; then
		ln -s $MPWD/tmuxifier/layouts/datafeeds.window.sh $mlocal/layouts/ 2> /dev/null
		echo 'linked datafeeds tmuxifier layout.'
	fi
	if [ ! -f $mldir/lib/oanda/oandapy/oandapy.py ]; then
		mkdir $mldir/lib/oanda/
		echo 'oandapy'
		git clone https://github.com/oanda/oandapy.git /ml.dev/lib/oanda/oandapy
		echo 'cloned oandapy.'
	fi
	if [ "`echo $PYTHONPATH | grep -i oandapy`" == "" ]; then
		export PYTHONPATH=$PYTHONPATH:/ml.dev/lib/oanda/oandapy
		echo 'adding path to Python path '
	fi
	if [ "`cat ~/.bashrc | grep -i oandapy`" == "" ]; then
		echo 'export PYTHONPATH=$PYTHONPATH:/ml.dev/lib/oanda/oandapy' >> ~/.bashrc
		echo 'adding PYTHONPATH export ~/.bashrc'
	fi
	echo ''
	echo 'install complete.'
}



if [ -d $mlocal ]; then
	minstall
else
	mdependencies
	minstall
fi
