from kafka import KafkaConsumer

bootstrap_servers = 'localhost:9092'
topics = ['results1', 'results2']

print(f"Listening on topics: {topics} ...")

consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=bootstrap_servers,
    group_id='results_consumer_group',
    auto_offset_reset='earliest',
    enable_auto_commit=False
)



try:
    for message in consumer:
        try:
            value = message.value.decode('utf-8')
        except Exception:
            value = message.value
        print(f"[{message.topic}] {value}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
