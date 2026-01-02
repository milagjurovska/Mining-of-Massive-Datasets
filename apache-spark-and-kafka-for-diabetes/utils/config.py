import os

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC_INPUT = 'health_data'
KAFKA_TOPIC_OUTPUT = 'health_data_predicted'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFLINE_DATA_PATH = os.path.join(BASE_DIR, "data", "offline.csv")
ONLINE_DATA_PATH = os.path.join(BASE_DIR, "data", "online.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_diabetes_model")
