from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import IntegerType, StringType, StructType

KAFKA_BOOTSTRAP_SERVERS = "10.98.116.24:9092"
KAFKA_TOPIC = "json_topic"

spark = SparkSession.builder.appName("count_month").getOrCreate()

# Reduce logging
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("id", IntegerType()) \
    .add("firstname", StringType()) \
    .add("middlename", StringType()) \
    .add("lastname", StringType()) \
    .add("dob_year", IntegerType()) \
    .add("dob_month", IntegerType()) \
    .add("gender", StringType()) \
    .add("salary", IntegerType())

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

person = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .groupBy("dob_month") \
    .count()

person.writeStream \
    .format("console") \
    .outputMode("complete") \
    .start() \
    .awaitTermination()


df.selectExpr("CAST(id AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .outputMode("append") \
    .option("kafka.bootstrap.servers", "10.98.116.24:9092")\
    .option("topic", "josn_data_topic") \
    .start() \
    .awaitTermination()