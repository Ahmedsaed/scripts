#!/bin/bash

# Set the maximum heap size based on the MEMORYSIZE environment variable
JAVA_OPTS="-Xmx${MEMORYSIZE} -Xms2G"

# Start the Minecraft server
java $JAVA_OPTS -jar server.jar nogui

