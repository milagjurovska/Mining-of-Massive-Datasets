#!/bin/bash
if [ -z "$KAFKA_HOME" ]; then
    echo "Please set KAFKA_HOME environment variable (e.g., export KAFKA_HOME=/path/to/kafka)"
    exit 1
fi
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
