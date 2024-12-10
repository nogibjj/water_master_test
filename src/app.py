import logging
from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count
import redis
from hashlib import sha256

# Initialize Flask app
app = Flask(__name__)

# Initialize SparkSession (global initialization)
spark = SparkSession.builder.appName("microservice").getOrCreate()
spark.sparkContext.setLogLevel("WARN")  # Reduce Spark logging

# Configure Redis for caching
cache = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@app.route("/process", methods=["POST"])
def process_data():
    """
    Receive JSON data stream, cache results, and return analysis.
    """
    try:
        logger.info("Received request to /process")
        data = request.get_json()
        cache_key = sha256(str(data).encode()).hexdigest()

        # Check if the result is cached
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Cache hit")
            return jsonify(eval(cached_result)), 200

        # Process data using Spark
        logger.info("Cache miss, processing data with Spark")
        df = spark.createDataFrame(data)
        result = df.groupBy("gender").agg(
            avg("salary").alias("average_salary"),
            count("*").alias("count")
        ).collect()

        # Convert results to JSON format
        result_json = [{"gender": row["gender"], "average_salary": row["average_salary"], "count": row["count"]} for row in result]

        # Store the result in cache
        cache.set(cache_key, str(result_json))

        return jsonify(result_json), 200
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# Entry point for Gunicorn
if __name__ != "__main__":
    logger.info("Gunicorn worker starting")
