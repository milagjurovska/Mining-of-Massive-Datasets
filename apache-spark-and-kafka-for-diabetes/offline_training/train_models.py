import os
import shutil
from utils.spark_session import get_spark_session
from offline_training.feature_engineering import assemble_features
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

def train_and_select_best_model(data_path, model_save_path):
    spark = get_spark_session("DiabetesOfflineTraining")
    df = spark.read.csv(data_path, header=True, inferSchema=True)
    data = assemble_features(df).select("features", "Diabetes_binary")
    train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

    evaluator = MulticlassClassificationEvaluator(labelCol="Diabetes_binary", predictionCol="prediction", metricName="f1")
    
    models = [
        ("LogisticRegression", LogisticRegression(labelCol="Diabetes_binary", featuresCol="features"), 
         ParamGridBuilder().addGrid(LogisticRegression.regParam, [0.01, 0.1]).build()),
        ("RandomForest", RandomForestClassifier(labelCol="Diabetes_binary", featuresCol="features"), 
         ParamGridBuilder().addGrid(RandomForestClassifier.numTrees, [10, 20]).build()),
        ("GBT", GBTClassifier(labelCol="Diabetes_binary", featuresCol="features"), 
         ParamGridBuilder().addGrid(GBTClassifier.maxIter, [10, 20]).build())
    ]

    best_f1 = 0
    best_model = None

    print(f"Training models using {data_path}...")
    for name, model, grid in models:
        print(f"  > Training {name}...")
        cv = CrossValidator(estimator=model, estimatorParamMaps=grid, evaluator=evaluator, numFolds=3)
        cv_model = cv.fit(train_data)
        f1 = evaluator.evaluate(cv_model.transform(test_data))
        if f1 > best_f1:
            best_f1 = f1
            best_model = cv_model.bestModel

    if best_model:
        print(f"Best model selected with F1: {best_f1:.4f}")
        if os.path.exists(model_save_path):
            shutil.rmtree(model_save_path)
        best_model.save(model_save_path)
        print(f"Model saved natively to {model_save_path}")
    
    spark.stop()

if __name__ == "__main__":
    train_and_select_best_model(r"data/offline.csv", r"models/best_diabetes_model")
