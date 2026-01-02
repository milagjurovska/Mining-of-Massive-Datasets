import pandas as pd
import json
import time
from kafka import KafkaProducer
from utils.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_INPUT, ONLINE_DATA_PATH

def start_producer():
    print(f"Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Loading data from {ONLINE_DATA_PATH}...")
    df = pd.read_csv(ONLINE_DATA_PATH).drop(columns=['Diabetes_binary'], errors='ignore')
    print(f"Starting to send {len(df)} records...")
    for i, row in df.iterrows():
        producer.send(KAFKA_TOPIC_INPUT, row.to_dict())
        if i % 10 == 0:
            print(f"Sent {i}/{len(df)} records...")
        time.sleep(0.5)
    producer.flush()
    producer.close()
    print("All records sent!")

if __name__ == "__main__":
    start_producer()
