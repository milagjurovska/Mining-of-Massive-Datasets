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

