# Mining of Massive Datasets

This repository contains all three homework assignments for the Intro to mining of massive datasets course.

## Homework 1
This assignment uses Apache Kafka and Apache Flink to simulate a data stream. Each data sent to the stream is in the following format:

``` {"key": "B", "value": 370, "timestamp": 1669748895562} ```

The result we get after successfully starting the Flink job is:

``` [results1] {"key":"B","window_start":1763845500000,"window_end":1763845560000,"cnt":5}```

```[results2] {"key":"D","window_start":1763775840000,"window_end":1763775900000,"min_value":31, "count":5,"average":444.0,"max_value":848} ```

## Homework 2
This project implements a collaborative filtering movie recommendation system using Apache Spark's ALS (Alternating Least Squares) algorithm, compared with alternative approaches from the Surprise library. It uses the **MovieLens Dataset** - Movie ratings and user preferences for recommendation system evaluation.

### Models Evaluated
- **Spark ALS** - RMSE: 0.920, MAE: 0.728 (Best performer)
- **Surprise SVD** - RMSE: 0.938, MAE: 0.739
- **Surprise KNN User-Based** - RMSE: 1.022, MAE: 0.809
- **Surprise KNN Item-Based** - RMSE: 1.037, MAE: 0.823

## Homework 3
Real-time diabetes prediction pipeline using Spark MLlib and Kafka on WSL (Linux).

## Overview
- **Offline Phase**: Trains Logistic Regression, Random Forest, and GBT models. Selects the best performing model (F1-score) and saves it in Spark Native format.
- **Online Phase**: Kafka producer streams health data; Spark Structured Streaming application performs real-time feature engineering and predictions.

## Offline Phase: Training Output
This output confirms that the model was trained successfully and saved in the native Spark format.
```
Training models using data/offline.csv...
  > Training LogisticRegression...
  > Training RandomForest...
  > Training GBT...
Best model selected with F1: 0.7502
Model saved natively to models/best_diabetes_model
```

## Online Phase: Streaming Output

### 1. Producer Output (Sending Data)
This output shows the producer reading health records from `online.csv` and sending them to the `health_data` Kafka topic.
```
Connecting to Kafka at localhost:9092...
Loading data from data/online.csv...
Starting to send 6400 records...
Sent 0/6400 records...
Sent 10/6400 records...
Sent 20/6400 records...
...
All records sent!
```

### 2. Consumer Output (Receiving Predictions)
This output from the consumer shows the real-time predictions made by the Spark application processing the producer's data.
```
Prediction: Diabetes Risk | Data: {'HighBP': 1.0, 'HighChol': 1.0, 'CholCheck': 1.0, 'BMI': 31.0, 'Smoker': 1.0, 'Stroke': 0.0, 'HeartDiseaseorAttack': 0.0, 'PhysActivity': 1.0, 'Fruits': 1.0, 'Veggies': 1.0, 'HvyAlcoholConsump': 0.0, 'AnyHealthcare': 1.0, 'NoDocbcCost': 0.0, 'GenHlth': 3.0, 'MentHlth': 0.0, 'PhysHlth': 30.0, 'DiffWalk': 0.0, 'Sex': 1.0, 'Age': 11.0, 'Education': 4.0, 'Income': 8.0, 'prediction': 1.0}
Prediction: Diabetes Risk | Data: {'HighBP': 0.0, 'HighChol': 0.0, 'CholCheck': 1.0, 'BMI': 26.0, 'Smoker': 1.0, 'Stroke': 0.0, 'HeartDiseaseorAttack': 0.0, 'PhysActivity': 1.0, 'Fruits': 1.0, 'Veggies': 1.0, 'HvyAlcoholConsump': 0.0, 'AnyHealthcare': 1.0, 'NoDocbcCost': 0.0, 'GenHlth': 4.0, 'MentHlth': 0.0, 'PhysHlth': 1.0, 'DiffWalk': 0.0, 'Sex': 0.0, 'Age': 13.0, 'Education': 6.0, 'Income': 5.0, 'prediction': 1.0}
Prediction: Healthy | Data: {'HighBP': 0.0, 'HighChol': 0.0, 'CholCheck': 1.0, 'BMI': 29.0, 'Smoker': 0.0, 'Stroke': 0.0, 'HeartDiseaseorAttack': 0.0, 'PhysActivity': 1.0, 'Fruits': 0.0, 'Veggies': 0.0, 'HvyAlcoholConsump': 0.0, 'AnyHealthcare': 1.0, 'NoDocbcCost': 0.0, 'GenHlth': 2.0, 'MentHlth': 0.0, 'PhysHlth': 2.0, 'DiffWalk': 0.0, 'Sex': 1.0, 'Age': 1.0, 'Education': 4.0, 'Income': 3.0, 'prediction': 0.0}
```

Each prediction shows whether the model predicts "Diabetes Risk" or "Healthy" based on health indicators like blood pressure, cholesterol, BMI, age, and lifestyle factors.
