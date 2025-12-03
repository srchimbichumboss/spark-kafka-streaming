from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, to_timestamp, from_unixtime
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, LongType

spark = SparkSession.builder \
    .appName("SensorDataAnalysis") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("sensor_id", IntegerType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("timestamp", LongType(), True)
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .option("startingOffsets", "earliest") \
    .load()

parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
with_ts = parsed.withColumn("ts", to_timestamp(from_unixtime(col("timestamp"))))

windowed_stats = with_ts \
    .groupBy(window(col("ts"), "1 minute"), col("sensor_id")) \
    .agg({"temperature": "avg", "humidity": "avg"}) \
    .select(col("window"), col("sensor_id"), col("avg(temperature)").alias("avg_temperature"), col("avg(humidity)").alias("avg_humidity"))

query = windowed_stats \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
