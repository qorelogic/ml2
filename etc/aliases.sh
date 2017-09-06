
# Aliases

alias ll='ls -l'
# turn color on for piping thru less (needs less -R option)
alias ls='ls --color'

alias mxi='. ~/.tmuxifier/test/test-helper.sh'
alias tmi='~/.tmuxifier/bin/tmuxifier'
alias mx='~/.tmuxifier/bin/tmuxifier'
mxew() {
	mx ew $1 && mx w $1
}
alias vg='vagrant'

# Use Vim As A Syntax Highlighting Pager (source: http://ubuntu-tutorials.com/2008/07/14/use-vim-as-a-syntax-highlighting-pager/)
alias vless='vim -u /usr/share/vim/vim71/macros/less.vim'

alias wn='watch -n1'
alias duu='du -bscm'
alias dfh='df -h'
alias nr='networkRestart'
alias no='sudo /etc/init.d/networking stop'
alias apr='/etc/init.d/apache2 restart'
alias apl='/etc/init.d/apache2 reload'
alias apc='apache2ctl'
alias apcs='apache2ctl -S'
alias a2e='a2ensite'
alias a2d='a2dissite'
alias lygo='lynx google.com'
alias pp='ping'
alias i='ifconfig'
alias ii='iwconfig'
alias rr='route -n'
alias ef='nano /home/qore/qorelogic/bin/functions.sh'
alias ei='nano /etc/network/interfaces'
alias en='nano /etc/init.d/networking'
alias re='route del -net 169.254.0.0 netmask 255.255.0.0'
alias txpower='iwlist txpower'
alias sq='sudo su qore'
#alias ipn='ipython notebook --pylab=inline' # deprecated
alias ipn='ipython notebook'

# enlightenment aliases
alias eff="enlightenment_filemanager "

#source: http://blackwinter.de/misc/etc/bash_aliases
alias al="alias | /bin/grep --color -F"

# i'm just too lazy, i know...
alias qoregrep="/bin/grep --color -rs --exclude *.svn-base"
#alias     grep="qoregrep -EHn"
alias     grep="grep --color=auto"
alias    fgrep="qoregrep -F"
alias    egrep="qoregrep -E"

alias diff="diff -C 0"

alias xmltidy="tidy -xml -i -w 0"

alias cdrecord="cdrecord dev=0,0,0 driveropts=burnproof -v -eject"

alias .cmp="copy-master-pass"
alias o="copy-master-pass"
alias oo="palimpsest"
alias .q21="qorelogic 2 2 2 1"
alias ppp="qorelogic 2 2 2 1" # right hand alias
alias  d="du -sch"
alias da="du -sch --apparent-size"
alias f="nano ~/qorelogic/bin/functions.sh"
alias l="nano ~/qorelogic/bin/libqore.sh"
alias s="nano ~/qorelogic/bin/server-management.sh"

alias pa="ps awwwux"
alias pe="ps -ef"
alias  h="host"
alias cl="clear; l"

alias  .a="apt-get "
alias .as="apt-cache search "
alias .aw="apt-get show"
alias .ai="sudo apt-get install"

alias .au="sudo apt-get update"
alias .uu="sudo apt-get update && sudo apt-get upgrade"
alias .uf="sudo apt-get update && sudo apt-get full-upgrade"
alias .ud="sudo apt-get update && sudo apt-get dist-upgrade"
alias .ar="sudo apt-get remove"
alias .ap="sudo apt-get purge"
alias .af="apt-file search"
alias .al="apt-file list"

alias  .g="gem"
alias .gs="gem search -b -d"
alias .gi="sudo gem install"
#alias .gr="sudo gem uninstall"
alias .go="gem outdated"
alias .gu="sudo gem update"
alias .gcl="sudo gem cleanup"
alias .ga="sudo gem sources --add"

alias .w1="wipe -rfqQ1 "
alias .wipe.pass1="wipe -rfqQ1 "
alias .wipe.pass7="wipe -rfqQ7 "
alias .wipe.pass15="wipe -rfqQ15 "
alias .wipe.pass32="wipe -rfqQ32 "
alias .dubs="du -bscm  "
#alias g="git" # just a git alias
alias .gis="git status" # show status
alias .gb="git branch -vv --color | less -SR"; alias gb=".gb" # list branches
alias .gba="git branch -a -vv --color | less -SR"; alias gba=".gba" # list branches
alias .gib="git branch -v " # list branches
alias .gch="git checkout" # switch to branch
alias .gch="git checkout"; alias gch=".gch" # switch to branch
alias .gici="git -a -m " # switch commit
alias .gidb="git -a -m " # delete branch
alias .gswitch="git remote set-url origin " # svn switch equivalent
alias .gch="git checkout -m " # switch merge to given branch
alias .gchp="git checkout -m - " # switch merge to previous branch
alias .gx="git checkout -m " # switch merge to given branch

alias sc='scrapy'

# source: http://stackoverflow.com/questions/2255416/how-to-determine-when-a-git-branch-was-created
.gmerge-base-gitk-all() {
	if [ "$1" == "" ] || [ "$2" == "" ]; then
		echo "usage: <branch-ref> <branch-base>"
	else
		gitk --all --select-commit=`git merge-base $1 $2` & 
	fi
}

.gpush() {
	currentBranch="`git branch | grep '\*' | cut -d':' -f3 | cut -c 3-`"                                                       
	echo "Pushing to branch $currentBranch.."
	if [ "$1" == "-f" ]; then
		goption="$1"
	else
		goption=""
	fi
	git push $goption origin $currentBranch:$currentBranch
	git push $goption --tags origin
}
.gpull() {
	currentBranch="`git branch | grep '\*' | cut -d':' -f3 | cut -c 3-`"                                                       
	echo "Pulling from branch $currentBranch.."
	git pull origin $currentBranch
}
.gpulli() {
	git stash && .gpull && git stash pop stash@{0}
}

.gfetch-setUpstreamTo() {
    if [ "$1" == "" ] || [ "$2" == "" ] || [ "$3" == "" ]; then
        echo "usage: <remote> <branch> <upstream>"
    else
        git fetch $1 $2:$2
        git branch --set-upstream-to=$3 $2
    fi
}

.gsweepPullPush() {
	nsleep=0
		if [ "$1" == "" ]; then
			echo ".gsweepPullPush <remote>"
		else
			gremote="$1"
        for i in `git branch | cut -c 3-`; do
		echo '';
		echo "== git checkout $i =============================================================";
		#git checkout $i;
		sleep $nsleep;
		echo "-- git pull $gremote $i:$i -----------------------------------------------------------";
		#.gpull;
		#git pull $gremote $i:$i
		sleep $nsleep;
		echo "-- git push $gremote $i:$i -----------------------------------------------------------";
		#.gpush;
		git push $gremote $i:$i
		sleep $nsleep;
		done
		fi
}

.grebaseWaterfall() {
	if [ "$1" == "" ] || [ "$2" == "" ]; then
		echo "usage: <from to>"
	else
		for i in `git branch | grep "$2" | xargs echo`; do

			echo "=========="
			echo ""
			echo -n "git rebase $1 $i; ? (y/n): "
			ans=""
			read ans
			if [ "$ans" == "y" ]; then
				echo "rebasing: git rebase $1 $i"
				git rebase $1 $i;
			fi

			echo "----------"
			echo ""
			echo -n "git push $i; ? (y/n): "
			ans=""
			read ans
			if [ "$ans" == "y" ]; then
				echo "pushing $i"
				.gpush

				echo ""
				echo -n "git push -f $i; [FORCE] ? (y/n): "
				ans=""
				read ans
				if [ "$ans" == "y" ]; then
					echo "force pushing $i"
					.gpush -f
				fi

			fi
		done
	fi
}

alias .gstl="git stash list "
.gstshow() {
	for x in `git stash list | cut -d'{' -f2 | cut -d'}' -f1`; do
		git stash show -p stash@{$x}; echo '';
	done
}
alias gsl='.gstl'
alias gss='.gstshow'

alias  .sl="svn log -r 1:HEAD"
alias  .slv="svn log --verbose -r 1:HEAD"
alias   .s="svn"
alias  .sa="svn add"
alias  .scl="svn commit "
alias  .si="svn info"
alias  .sci=".si && svn commit"
alias  .sw="svn switch"
alias  .sc="svn cleanup"
alias  .sd="svn diff --diff-cmd=colordiff"
alias  .sdl="svn diff --diff-cmd=colordiff | less -SR"
alias  .sdc="svn diff --diff-cmd=diff $1 | kompare -o -"
alias  .sH="svn diff -rHEAD"
alias  .sP="svn diff -rPREV"
alias  .sdf="svn diff | less -SR"
alias  .dd="for c in \$(.sC); do .sd \$c; done"
alias  .sr="svn revert "
alias  .srr="svn revert --recursive ."
alias  .srr="svn revert --recursive ."
alias  .sm="svn mkdir"
alias  .so="svn checkout"
alias  .ss="svn status"
alias  .sss="svn status --show-updates"
alias  .su="svn update"
alias  .sv="svn status | /bin/grep '^\?' | awk '{print \$2}'"         # get unversioned files
alias  .sc="svn status | /bin/grep '^[AM]' | sed 's/.* //'"           # get modified files
alias  .sI="svn status --no-ignore | /bin/grep '^I' | sed 's/.* //'"  # get ignored files
alias  .du="dos2unix"
alias  .ud="unix2dos"

alias sedGit2Perforce="sed -e 's/git/perforce/g'"
#alias sg2p="sedGit2Perforce"
alias sg2p="grep -v git | perl -pe 's/^.*?:\d+://g'"

alias .gib="git init --bare | sg2p"
alias .gi="git init | sg2p"
alias .gstat="git status | sg2p"
alias .gstatl="git status | sg2p | less -SR"
alias .gd="git diff --color | sg2p"
alias .gdb="git diff --color "
alias .gdl="git diff --color | less -SR"
alias .ga="git add | sg2p"
# source: http://stackoverflow.com/questions/1838873/visualizing-branch-topology-in-git
gformat="--format=format:'%C(bold blue)%h%C(reset) - %an%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %C(auto)%d%C(reset)'"
gformat2="--format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(auto)%d%C(reset)%n''           %an%C(reset) - %C(white)%s%C(reset) %C(dim white)'"
#alias .gl=" git log --all --decorate --graph $gformat | sg2p | less"
alias .gl="  git log --decorate --graph $gformat --numstat --parents"
alias .glp=" git log --decorate --graph $gformat --parents -p"
alias .glo=" git log --decorate --graph --oneline --parents $gformat"
alias .glo2=" git log --decorate --graph --oneline --parents $gformat2"
alias .glon="git log --all --decorate --oneline $gformat --parents --numstat"
alias .gla=" git log --all --decorate --graph $gformat | sg2p | less -SR"
alias gl=".gl"
alias gla=".gl --all"
alias glp=".glp"
alias glpa=".glp --all"
alias glo=".glo"
alias gloa=".glo --all"
alias glo2=".glo2"
alias glo2a=".glo2 --all"
alias lo=".glo"
alias loa="gloa"; alias llo="loa"; 
alias lo2=".glo2"
alias lo2a="glo2a"
# list git tag annotation messages
alias .gt="git tag -ln99"
# fetch and push remote tags
alias .gtpull="git fetch origin --tags"
alias .gtpush="git push origin --tags"
alias .gci=".gb && sleep 0 && git commit -m "
alias .gcini="git commit -m "
alias .ga="git add -i "; alias ga=".ga "
alias .grh="git reset --hard "
.grhi() {
  if [ "$1" == "" ]; then
        echo "usage: <git hash>"
  else
	git stash && git reset --hard $1 && git stash pop stash@{0}
  fi
}

alias .gri="git rebase -i "
alias .gr="git remote -v" # list remotes
# quick git rebase -i HEAD~n method
.gfb() {
	if [ "$1" == "" ] || [ "$2" == "" ]; then
	echo "usage: <remote> <branch>"
	else
	git stash
	git checkout -m -
	git fetch $1 $2:$2
	git checkout -m -
	git stash pop stash@{0}
	fi
}
grin() {
	if [ "$1" == "" ]; then
	echo "usage: <number of commuits>"
	else
	#git rebase -i HEAD~$1
	#git rebase -i -v HEAD~$1
	git rebase -i --stat HEAD~$1
	fi
}
alias .grin="grin "
alias .gra="git commit --amend"
alias .grc="git rebase --continue"
alias .gc="git commit "
alias .gca="git commit --amend"
alias .gcp="git cherry-pick "
.gcpbatch() {
	for i in `echo "$@"`; do
		#echo $i;
		git log --oneline -n 1 $i
		#ans=`read 'ansss'`
		echo -n "cherry-pick $i? (y/n): "
                read ans
                echo "res: $ans"
		if [ "$ans" == "y" ]; then
			.gcp $i
		fi
	done
}

alias .gacpush='.ga && .gc && .gpush'

# source: http://stackoverflow.com/questions/21168846/cant-remove-file-from-git-commit
#alias .g-remove-from-commit="git filter-branch -f --index-filter "git rm -rf --cached --ignore-unmatch FOLDERNAME" -- --all "

alias    .p="perl"

alias   .pe="perl -le"
alias   .pd="perldoc"
alias  .pdf="perldoc -f"
alias  .pdq="perldoc -q"
alias .pdep="perl -d:Modlist=stop"
alias   .pc="perl -Mlib=lib -c"
alias   .pt="./Build test --verbose 1 --test_files"

# show more info
alias whois="whois -H -T dn"

# One needs to set -Kn when he wants to put iso-8859 letters. matz.
#alias ruby="ruby -Kn"
alias ruby="ruby -Ku"

# use fastri, always
#alias ri="fri"

# home paths
alias .ghml='cd /mldev/bin'
alias .ghmllive='cd /mllive/bin'

# https://help.ubuntu.com/community/IptablesHowTo
qiptables-list() {
	fname="/tmp/iptables"
	sudo sh -c "iptables-save > $fname"
	cat $fname
}
qiptables() {
	sudo iptables -vL -t filter
	sudo iptables -vL -t nat
	sudo iptables -vL -t mangle
	sudo iptables -vL -t raw
	sudo iptables -vL -t security
}

# source: http://stackoverflow.com/questions/12399002/how-to-configure-git-bash-command-line-completion
# In my Ubuntu 14.04 this file is /usr/share/bash-completion/completions/git . /etc/bash_completion.d/git-prompt is used for git prompt support, not for completion
echo 'bash completions'
#source /usr/share/bash-completion/completions/git 

# alias git to g [with bash completion]
# source: http://askubuntu.com/questions/62095/how-to-alias-git-to-g-so-that-bash-completion-rules-are-preserved
echo 'alias git to g'
complete -o bashdefault -o default -o nospace -F _git g 2>/dev/null || complete -o default -o nospace -F _git g
#complete -o bashdefault -o default -o nospace -F git g 2>/dev/null || complete -o default -o nospace -F git g
#alias g='git'
#source /usr/share/bash-completion/completions/git

qnato-phonetic() {
	#eog /mldev/assets/art/Desktop/350px-FAA_Phonetic_and_Morse_Chart2.svg.png
	eog /mldev/assets/art/nato-phonetic-hS7467E.jpg
}
