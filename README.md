 repositorio

0: Spark Streaming con Kafka

Este proyecto implementa análisis de datos en tiempo real usando . Kafka y se procesan en tiempo real con Spark.

---

0:  Generalidades
- Python 3.x
- Apache Spark (3.5.x)
- Apache Kafka (3.x)
- Librería `kafka-python`
- Máquina virtual con Ubuntu y Hadoop (según instructivo)

---

  0:Preparación del entorno
1. Conectarse por SSH a la máquina virtual:
   ```bash
   ssh vboxuser@<IP_VM>
pip install kafka-python

wget https://downloads.apache.org/kafka/3.6.2/kafka_2.13-3.6.2.tgz
tar -xzf kafka_2.13-3.6.2.tgz
sudo mv kafka_2.13-3.6.2 /opt/Kafka


0: ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

0: Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data
python3 kafka_producer.py

python3 kafka_producer.py


---
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &


/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data

python3 kafka_producer.py

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumer.py

http://192.168.0.136:4040

Configuracion de broker:✌️

0_ /opt/Kafka/config/server.properties (fragmentos clave)
listeners=PLAINTEXT://0.0.0.0:9092
advertised.listeners=PLAINTEXT://192.168.10.36:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT
inter.broker.listener.name=PLAINTEXT
zookeeper.connect=localhost:2181

2.Productor kafka:🤷‍♂️

0:kafka_producer.py
import time
import json
import random
from kafka import KafkaProducer

def generate_sensor_data():
    return {
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "timestamp": int(time.time())   # epoch en segundos
    }

producer = KafkaProducer(
    bootstrap_servers=['192.168.10.36:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

while True:
    sensor_data = generate_sensor_data()
    producer.send('sensor_data', value=sensor_data)
    print(f"Sent: {sensor_data}")
    time.sleep(1)
3.Consumidor:

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, from_unixtime, to_timestamp, avg
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, LongType

spark = (SparkSession.builder
         .appName("KafkaSparkStreaming")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

# Esquema JSON de entrada
schema = StructType([
    StructField("sensor_id", IntegerType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("timestamp", LongType(), True)   # epoch en segundos
])

# Fuente Kafka (Structured Streaming)
df = (spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.10.36:9092")
      .option("subscribe", "sensor_data")
      .option("startingOffsets", "earliest")
      .load())

# Parseo y tiempo de evento (segundos → timestamp)
parsed = (df
          .select(from_json(col("value").cast("string"), schema).alias("data"))
          .select("data.*")
          .withColumn("event_time", to_timestamp(from_unixtime(col("timestamp"))))
          .withWatermark("event_time", "2 minutes"))

# Ventanas de 1 minuto por sensor, promedios
windowed = (parsed
            .groupBy(window(col("event_time"), "1 minute"), col("sensor_id"))
            .agg(
                avg("temperature").alias("avg_temperature"),
                avg("humidity").alias("avg_humidity")
            ))

# Consola (complete) para ver estado agregado
query_console = (windowed.writeStream
                 .outputMode("complete")
                 .format("console")
                 .option("truncate", "false")
                 .start())

# Parquet (append) + checkpoint (exactly-once y recuperación)
query_parquet = (windowed.writeStream
                 .outputMode("append")
                 .format("parquet")
                 .option("path", "out/stream/metrics")
                 .option("checkpointLocation", "out/stream/_chk")
                 .start())

spark.streams.awaitAnyTermination()


0: spark_streaming_consumer.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, from_unixtime, to_timestamp, avg
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, LongType

spark = (SparkSession.builder
         .appName("KafkaSparkStreaming")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

0: Esquema del JSON de entrada
schema = StructType([
    StructField("sensor_id", IntegerType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("timestamp", LongType(), True)   # epoch en segundos
])

0: Fuente Kafka (Structured Streaming)
df = (spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.10.36:9092")
      .option("subscribe", "sensor_data")
      .load())

0: Parseo y tiempo de evento (segundos → timestamp)
parsed = (df
          .select(from_json(col("value").cast("string"), schema).alias("data"))
          .select("data.*")
          .withColumn("event_time", to_timestamp(from_unixtime(col("timestamp"))))
          .withWatermark("event_time", "2 minutes"))

0: Ventanas de 1 minuto por sensor, promedios
windowed = (parsed
            .groupBy(window(col("event_time"), "1 minute"), col("sensor_id"))
            .agg(
                avg("temperature").alias("avg_temperature"),
                avg("humidity").alias("avg_humidity")
            ))

0: Consola (complete) para ver estado agregado
query_console = (windowed.writeStream
                 .outputMode("complete")
                 .format("console")
                 .option("truncate", "false")
                 .start())

0: Parquet (append) + checkpoint (exactly-once y recuperación)
query_parquet = (windowed.writeStream
                 .outputMode("append")
                 .format("parquet")
                 .option("path", "out/stream/metrics")
                 .option("checkpointLocation", "out/stream/_chk")
                 .start())

spark.streams.awaitAnyTermination()
5. Ejecutar:👌

1.Arrancar ZooKeeper 👍
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

 2. Arrancar Kafka👌
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

  3. Validar el tópico👍
/opt/Kafka/bin/kafka-topics.sh --bootstrap-server 192.168.10.36:9092 --list

   4. Producer 👌
python3 kafka_producer.py

   5) Consumer (Spark Streaming + Kafka👌)
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
  spark_streaming_consumer.py
6.Validacionde flujo:
(Codigo):ls -la out/stream/metrics | head
      )Lectura del batch👌):
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("LeerParquet").getOrCreate()
df = spark.read.parquet("out/stream/metrics")
df.orderBy("sensor_id").show(40, truncate=False)
spark.stop()


