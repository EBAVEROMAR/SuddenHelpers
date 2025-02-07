#sudo apt update
# sudo apt install kafka
#
#Start Kafka Server
#zookeeper-server-start.sh config/zookeeper.properties
# kafka-server-start.sh config/server.properties
# Create a topic
# kafka-topics.sh --create --topic mmwave_data --bootstrap-server localhost:9092
#
# sudo apt update
# sudo apt install influxdb
#
# Start InfluxDB
# influxd
# Create InfluxDB database
# influx
# CREATE DATABASE mmwave

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt

# InfluxDB Setup
db_client = InfluxDBClient(host='localhost', port=8086)
db_client.switch_database('mmwave')

# MQTT Setup
MQTT_BROKER = "192.168.1.100"
MQTT_TOPIC = "sensor/mmwave"

def on_message(client, userdata, message):
    value = float(message.payload.decode())
    json_body = [{
        "measurement": "vital_signs",
        "fields": {"sensor_value": value}
    }]
    db_client.write_points(json_body)

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
client.loop_forever()

# Open Grafana (default: http://localhost:3000)
# Add Data Source → Select InfluxDB
# Set URL to http://localhost:8086 and database as mmwave
# Create a new dashboard and visualize sensor data!