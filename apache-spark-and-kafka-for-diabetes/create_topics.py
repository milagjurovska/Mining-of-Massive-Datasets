from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")

topics = [
    NewTopic(name="health_data", num_partitions=1, replication_factor=1),
    NewTopic(name="health_data_predicted", num_partitions=1, replication_factor=1)
]

try:
    admin_client.create_topics(new_topics=topics, validate_only=False)
    print("Topics created successfully!")
except Exception as e:
    print(f"Topics may already exist or error occurred: {e}")

admin_client.close()
