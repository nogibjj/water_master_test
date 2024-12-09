from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min, count, when, desc, countDistinct
from pyspark.sql.window import Window

KAFKA_BOOTSTRAP_SERVERS = "10.98.116.24:9092"
KAFKA_TOPIC = "emp_data"

spark = SparkSession.builder.appName("json_data_analysis").getOrCreate()

# Reduce logging
spark.sparkContext.setLogLevel("WARN")

# Define the schema for the JSON data
schema = (
    "id INT, name STRING, age INT, gender STRING, occupation STRING, "
    "salary DOUBLE, birth_date DATE, city STRING, country STRING, "
    "education STRING, years_of_experience INT, is_manager BOOLEAN"
)

# Read the JSON data from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Convert the value column from binary to string and parse the JSON data
df = df.selectExpr("CAST(value AS STRING)")
df = df.selectExpr("from_json(value, '{}') as data".format(schema)).select("data.*")

# Perform data analysis on the JSON data
analysis_df = df.select(
    avg("salary").alias("average_salary"),
    max("age").alias("max_age"),
    min("age").alias("min_age"),
    count("id").alias("record_count"),
    count(when(col("gender") == "M", 1)).alias("male_count"),
    count(when(col("gender") == "F", 1)).alias("female_count"),
    count(when(col("is_manager") == True, 1)).alias("manager_count"),
    avg("years_of_experience").alias("average_years_of_experience")
)

# Calculate top N most common names
top_n_names = df.groupBy("years_of_experience").count().orderBy(desc("count"))

top_n_names.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query = analysis_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()