#!/bin/bash
xrandr --output eDP-1 --brightness .8 --primary --auto --output HDMI-1 --auto --above eDP-1 &
brightnessctl s 1% &
picom --experimental-backends -b &
amixer sset Speaker unmute 
# xset s on -dpms & 