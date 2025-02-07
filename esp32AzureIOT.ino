#include <WiFi.h>
#include <PubSubClient.h>

// WiFi Credentials
const char* ssid = "Your_WiFi_SSID";
const char* password = "Your_WiFi_Password";

// Azure IoT Hub Credentials
const char* mqtt_broker = "your-iot-hub.azure-devices.net";
const char* device_id = "esp32-mmwave";
const char* mqtt_username = "your-iot-hub.azure-devices.net/esp32-mmwave/?api-version=2021-04-12";
const char* mqtt_password = "Your_IoT_Hub_SAS_Token"; // Generate in Azure Portal

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    client.setServer(mqtt_broker, 8883);
    while (!client.connect(device_id, mqtt_username, mqtt_password)) {
        Serial.println("Trying to connect to Azure...");
        delay(2000);
    }
    Serial.println("Connected to Azure IoT Hub");
}

void loop() {
    if (!client.connected()) {
        client.connect(device_id, mqtt_username, mqtt_password);
    }

    // Simulated mmWave sensor data
    float heartRate = random(60, 100); 
    float respirationRate = random(12, 20); 

    String payload = "{ \"heartRate\": " + String(heartRate) + ", \"respirationRate\": " + String(respirationRate) + " }";
    client.publish("devices/esp32-mmwave/messages/events/", payload.c_str());

    Serial.println("Data sent: " + payload);
    delay(5000);
}
