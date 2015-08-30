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
	if [ ! -f $mlocal/layouts/qlm.window.sh ]; then
		echo "$mlocal/layouts contents:"
		ls -l $mlocal/layouts
		echo "need to fix $mlocal/layouts, sure you want to remove directory $mlocal/layouts? y/n: "
		read ans
		if [ "$ans" == "y" ]; then
			rm -rfv $mlocal/layouts
			ln -s $MPWD/../tmuxifier/layouts $mlocal/layouts 2> /dev/null
			echo 'linked mldev/bin/tmuxifier/layouts to ~/.tmuxifier/layouts'
		fi
	fi
	if [ ! -f $mldir/lib/oanda/oandapy/oandapy.py ]; then
		mkdir -p $mldir/lib/oanda/
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

	# python packages for datafeeds
	if [ "`python -c 'import QSTK' 2>&1`" != "" ]; then
            sudo pip install QSTK
	fi
	if [ "`python -c 'import Quandl' 2>&1`" != "" ]; then
            sudo pip install Quandl
	fi
	if [ "`python -c 'import html2text' 2>&1`" != "" ]; then
            sudo pip install html2text
	fi
	if [ "`python -c 'import selenium' 2>&1`" != "" ]; then
            sudo pip install selenium
	fi

	# still testing on ipython notebook
      if [ "`python -c 'import bitstampy' 2>&1`" != "" ]; then
            sudo pip install bitstampy
	fi
      if [ "`python -c 'import krakenex' 2>&1`" != "" ]; then
            sudo pip install krakenex
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
