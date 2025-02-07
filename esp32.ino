#include <WiFi.h>
#include <PubSubClient.h>
#include <HardwareSerial.h>

// WiFi and MQTT Config
const char* ssid = "Your_WiFi_SSID";
const char* password = "Your_WiFi_Password";
const char* mqtt_server = "192.168.1.100"; // Replace with your PC's IP (running Mosquitto/Kafka bridge)
const int mqtt_port = 1883; 

WiFiClient espClient;
PubSubClient client(espClient);

// Serial Port for mmWave Sensor
HardwareSerial mmWaveSerial(1);

void setup() {
    Serial.begin(115200);
    mmWaveSerial.begin(115200, SERIAL_8N1, 16, 17); // TX=17, RX=16

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Connect to MQTT Broker
    client.setServer(mqtt_server, mqtt_port);
    while (!client.connected()) {
        if (client.connect("ESP32_Client")) {
            Serial.println("Connected to MQTT Broker");
        } else {
            Serial.print("Failed, retrying...");
            delay(2000);
        }
    }
}

void loop() {
    if (!client.connected()) {
        client.connect("ESP32_Client");
    }
    client.loop();

    if (mmWaveSerial.available()) {
        String data = mmWaveSerial.readStringUntil('\n'); // Read from sensor
        Serial.println("Publishing: " + data);
        client.publish("sensor/mmwave", data.c_str()); // Send to MQTT topic
    }
}
