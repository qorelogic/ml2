#!/bin/bash

clear

tmux set-option -g remain-on-exit off
#tmux new-session -d 'vi /tmp/passwd' \;
#nuu="`tmux new-session -d -P '/bin/bash -c \"/home/qore/.tmuxifier/bin/tmuxifier list\"'`" #\; split-window -d \; attach #-t 0
#tmux new-session -d -P '/bin/bash -c \"/home/qore/.tmuxifier/bin/tmuxifier w db\"' #\; split-window -d -P \; attach #-t 0
nuu="`tmux new-session -d -P '/bin/bash'`"

#tmux new-window '/bin/bash -c "/home/qore/.tmuxifier/bin/tmuxifier w db"; sleep 1'

#xeyes
#xeyes -geometry 1000x1000+0+0
#xterm -geometry "175x40+150+0" &

#echo $nuu
gnome-terminal --geometry "150x40+150+0" -x tmux attach -t $nuu 2> /dev/null &

