import os
import platform
import sys
import pyspark
from pyspark.sql import SparkSession

def get_spark_session(app_name="DiabetesPrediction"):
    is_windows = platform.system() == "Windows"

    if is_windows:
        if "JAVA_HOME" not in os.environ:
            os.environ["JAVA_HOME"] = r"C:\Java\jdk-17"
        os.environ["HADOOP_HOME"] = r"C:\hadoop"
        java_bin = os.path.join(os.environ["JAVA_HOME"], "bin")
        hadoop_bin = os.path.join(os.environ["HADOOP_HOME"], "bin")
        os.environ["PATH"] = java_bin + os.pathsep + hadoop_bin + os.pathsep + os.environ["PATH"]

    os.environ["SPARK_HOME"] = os.path.dirname(pyspark.__file__)
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    builder = SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")

    if is_windows:
        builder = builder \
            .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem") \
            .config("spark.hadoop.io.native.lib", "false") \
            .config("spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs", "false") \
            .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
            .config("spark.driver.extraJavaOptions", "-Djava.library.path=C:/hadoop/bin")

    return builder.getOrCreate()
