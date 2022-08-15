#!/bin/bash

# open meeting link in browser
day=$( date +%d )

while [ "$day" = "15" ]; 
do
    currenttime=$(date +"%H:%M")
    echo "Checking day 15 time:" "$currenttime"
    if [[ "$currenttime" > "19:55" ]] || [[ "$currenttime" < "00:30" ]]
    then
       echo "Running at " "$currenttime"
       python3 -m webbrowser "MEETING LINK" & > /dev/null 2> /dev/null
       # start recording
       /bin/bash /home/ahmed/scripts/obs/obs-toggle-recording.sh 3600 true
       sleep 60
       break
    else
       sleep $(( 15*60 ))
    fi
done

sleep $(( 6*60*60 ))
day=$( date +%d )

while [ "$day" = "16" ]; 
do
    currenttime=$(date +"%H:%M")
    echo "Checking day 15 time:" "$currenttime"
    if [[ "$currenttime" > "19:55" ]] || [[ "$currenttime" < "00:30" ]]
    then
       echo "Running at " "$currenttime"
       python3 -m webbrowser "MEETING LINK" & > /dev/null 2> /dev/null
       # start recording
       /bin/bash /home/ahmed/scripts/obs/obs-toggle-recording.sh 3600 true
       sleep 60
       break
    else
       sleep $(( 15*60 ))
    fi
done
