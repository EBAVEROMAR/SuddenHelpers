import requests
import json

ANOMALY_API = "https://your-anomaly-detector.cognitiveservices.azure.com/anomalydetector/v1.0/timeseries/entire/detect"
HEADERS = {"Ocp-Apim-Subscription-Key": "your_api_key", "Content-Type": "application/json"}

def detect_anomaly(sensor_data):
    data = {
        "series": [{"timestamp": entry["timestamp"], "value": entry["heartRate"]} for entry in sensor_data],
        "granularity": "second"
    }
    response = requests.post(ANOMALY_API, headers=HEADERS, json=data)
    return response.json()

# Example Data
sensor_data = [{"timestamp": "2025-02-05T12:00:00Z", "heartRate": 90}, {"timestamp": "2025-02-05T12:00:01Z", "heartRate": 50}]
anomalies = detect_anomaly(sensor_data)

print(anomalies)
