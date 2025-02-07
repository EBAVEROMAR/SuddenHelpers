import json
import requests
from azure.cosmos import CosmosClient

# Cosmos DB Configuration
COSMOS_URL = "https://your-cosmos-db.documents.azure.com:443/"
COSMOS_KEY = "your_primary_key"
DATABASE_NAME = "VitalSignsDB"
CONTAINER_NAME = "Anomalies"

# Initialize Cosmos DB Client
client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def store_anomaly(data):
    # Save anomaly details in Cosmos DB
    anomaly_entry = {
        "id": data["timestamp"],
        "heartRate": data["heartRate"],
        "respirationRate": data["respirationRate"],
        "anomalyDetected": True
    }
    container.create_item(anomaly_entry)
    print("Anomaly logged in Cosmos DB.")

# Example anomaly detection event
sensor_data = {"timestamp": "2025-02-05T12:00:01Z", "heartRate": 50, "respirationRate": 8}
store_anomaly(sensor_data)
