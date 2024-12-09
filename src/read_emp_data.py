from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min, count

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

df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
