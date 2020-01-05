#!/bin/sh

feh --bg-scale ~/Sync/pictures/Nord_Buck.jpg &
syncthing &
setxkbmap -option ctrl:nocaps &
xcape -e 'Control_L=Escape'

