#!/bin/bash

gtk-launch com.obsproject.Studio.desktop > /dev/null 2> /dev/null & # Launch obs and redirect stdout and stderr to null (don't print on screen)
sleep 1
obs-cli recording toggle --password as2652003 & # start recording 

# stop recording if an argument (time in seconds) is given
if [ $1 -gt 0 ]
then
    sleep $1
    obs-cli recording toggle --password as2652003 &
fi

trap "echo exiting" SIGTERM # kill obs without killing this script 

if [ "$2" = "true" ]
then
	sleep $((($1/60) * 600 + 5)) # give it some time to remux, each hour adds 10 minutes, with additional 5 seconds as a base
	pkill obs
fi
