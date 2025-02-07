EVENT_GRID_TOPIC_URL = "https://your-eventgrid-topic.westus-2.eventgrid.azure.net/api/events"
EVENT_GRID_KEY = "your_event_grid_key"

def trigger_anomaly_event(sensor_data):
    event = [{
        "id": sensor_data["timestamp"],
        "eventType": "mmWave.AnomalyDetected",
        "subject": "mmWaveSensor/Anomaly",
        "eventTime": sensor_data["timestamp"],
        "data": sensor_data,
        "dataVersion": "1.0"
    }]

    headers = {
        "aeg-sas-key": EVENT_GRID_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(EVENT_GRID_TOPIC_URL, headers=headers, json=event)
    
    if response.status_code == 200:
        print("Anomaly event triggered successfully!")
    else:
        print("Failed to trigger event:", response.text)

# Example Trigger
sensor_data = {"timestamp": "2025-02-05T12:00:01Z", "heartRate": 50, "respirationRate": 8}
trigger_anomaly_event(sensor_data)
