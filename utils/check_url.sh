#!/bin/bash

URL=$1 # Replace with your URL
COMMAND="notify 'link is up'" # Replace with your desired command

while true; do
  # Make a request and capture the status code
  STATUS_CODE=$(curl -L -o /dev/null -s -w "%{http_code}" $URL)

  # Check if the status code is 200
  if [ $STATUS_CODE -eq 200 ]; then
    # Run the desired command
    eval $COMMAND
    break
  else
    echo "Got $STATUS_CODE, Waiting for the URL to respond with 200..."
  fi

  # Wait for a short period before retrying (e.g., 5 seconds)
  sleep 5
done
