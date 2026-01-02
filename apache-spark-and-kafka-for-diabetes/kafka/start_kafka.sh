#!/bin/bash
if [ -z "$KAFKA_HOME" ]; then
    echo "Please set KAFKA_HOME environment variable"
    exit 1
fi
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
