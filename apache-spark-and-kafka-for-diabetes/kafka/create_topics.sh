#!/bin/bash
if [ -z "$KAFKA_HOME" ]; then
    echo "Please set KAFKA_HOME environment variable"
    exit 1
fi
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic health_data
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic health_data_predicted
