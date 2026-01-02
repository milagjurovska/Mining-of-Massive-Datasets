from kafka import KafkaConsumer
import json
from utils.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_OUTPUT

def start_result_consumer():
    import time
    print(f"Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
    print(f"Listening for predictions on topic '{KAFKA_TOPIC_OUTPUT}'...")
    print("Waiting for messages... (Press Ctrl+C to stop)\n")
    consumer = KafkaConsumer(
        KAFKA_TOPIC_OUTPUT,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        auto_offset_reset='earliest',
        group_id=f'result_viewer_{int(time.time())}',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    try:
        for message in consumer:
            data = message.value
            status = "Diabetes Risk" if data.get('prediction') == 1.0 else "Healthy"
            print(f"Prediction: {status} | Data: {data}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    start_result_consumer()
