import json
import requests
from azure.iot.hub import IoTHubRegistryManager

FHIR_SERVER = "https://your-fhir-server.azurehealthcareapis.com"
FHIR_TOKEN = "your_fhir_api_token"

def iothub_handler(event):
    for message in event.get_body():
        data = json.loads(message)
        fhir_data = {
            "resourceType": "Observation",
            "status": "final",
            "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
            "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]},
            "valueQuantity": {"value": data["heartRate"], "unit": "bpm"}
        }

        headers = {"Authorization": f"Bearer {FHIR_TOKEN}", "Content-Type": "application/json"}
        requests.post(f"{FHIR_SERVER}/Observation", json=fhir_data, headers=headers)
