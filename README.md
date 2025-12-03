# Mi primer repositorio

# Spark Streaming con Kafka

Este proyecto implementa análisis de datos en tiempo real usando **Apache Spark Streaming** y **Apache Kafka**. Se simulan datos de sensores que se envían a un *topic* en Kafka y se procesan en tiempo real con Spark.

---

## ✅ Requisitos
- Python 3.x
- Apache Spark (3.5.x)
- Apache Kafka (3.x)
- Librería `kafka-python`
- Máquina virtual con Ubuntu y Hadoop (según instructivo)

---

## ✅ Preparación del entorno
1. Conectarse por SSH a la máquina virtual:
   ```bash
   ssh vboxuser@<IP_VM>
pip install kafka-python

wget https://downloads.apache.org/kafka/3.6.2/kafka_2.13-3.6.2.tgz
tar -xzf kafka_2.13-3.6.2.tgz
sudo mv kafka_2.13-3.6.2 /opt/Kafka


# ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data
python3 kafka_producer.py

python3 kafka_producer.py


---

## ✅ Iniciar servicios
```bash
# ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &


/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data

python3 kafka_producer.py

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumer.py

http://192.168.0.134:4040
