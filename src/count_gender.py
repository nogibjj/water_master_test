import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import IntegerType, StringType, StructType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = "10.98.116.24:9092"
KAFKA_TOPIC = "json_topic"

# Initialize SparkSession
spark = SparkSession.builder.appName("count_gender").getOrCreate()

# Reduce Spark log verbosity
spark.sparkContext.setLogLevel("WARN")

# Define schema for incoming data
schema = StructType() \
    .add("id", IntegerType()) \
    .add("firstname", StringType()) \
    .add("middlename", StringType()) \
    .add("lastname", StringType()) \
    .add("dob_year", IntegerType()) \
    .add("dob_month", IntegerType()) \
    .add("gender", StringType()) \
    .add("salary", IntegerType())

logger.info("Starting to read stream from Kafka")

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

logger.info("Stream initialized successfully")

person = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .groupBy("gender") \
    .count()

logger.info("Grouped data by gender and started writing to console")

person.writeStream \
    .format("console") \
    .outputMode("complete") \
    .start() \
    .awaitTermination()
