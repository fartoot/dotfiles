#!/bin/bash
xrandr --output eDP-1 --primary --auto --output HDMI-1 --auto --above eDP-1 &
picom --experimental-backends &
amixer sset Speaker unmute
# Todour &
