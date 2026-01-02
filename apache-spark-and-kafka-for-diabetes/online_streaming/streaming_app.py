import os
from pyspark.sql.functions import from_json, col, to_json, struct
from utils.spark_session import get_spark_session
from utils.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_INPUT, KAFKA_TOPIC_OUTPUT, MODEL_PATH
from online_streaming.schema import get_health_data_schema
from offline_training.feature_engineering import assemble_features
from pyspark.ml.classification import LogisticRegressionModel, RandomForestClassificationModel, GBTClassificationModel

def start_streaming():
    spark = get_spark_session("DiabetesStreamingApp")
    
    # Generic loader attempt or specific if known. Using LR as primary example, 
    # but in a real app would use PipelineModel for transparency.
    try:
        model = LogisticRegressionModel.load(MODEL_PATH)
    except:
        try:
            model = RandomForestClassificationModel.load(MODEL_PATH)
        except:
            model = GBTClassificationModel.load(MODEL_PATH)

    schema = get_health_data_schema()
    
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC_INPUT) \
        .option("startingOffsets", "latest") \
        .load()
    
    json_df = streaming_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    
    data_with_features = assemble_features(json_df)
    predictions = model.transform(data_with_features)
    
    result_df = predictions.select([c.name for c in schema.fields] + ["prediction"])
    kafka_output_df = result_df.select(to_json(struct("*")).alias("value"))
    
    query = kafka_output_df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("topic", KAFKA_TOPIC_OUTPUT) \
        .option("checkpointLocation", "checkpoint") \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    start_streaming()
