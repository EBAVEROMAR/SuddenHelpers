import json
import requests

# Twilio API Configuration
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE = "+1234567890"  # Your Twilio number
USER_PHONE = "+351xxxxxxxxx"  # User's phone number

def send_sms_alert(sensor_data):
    message = f"🚨 ALERT: Anomaly detected!\nHeart Rate: {sensor_data['heartRate']} bpm\nRespiration Rate: {sensor_data['respirationRate']} breaths/min\nTimestamp: {sensor_data['timestamp']}"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    data = {
        "From": TWILIO_PHONE,
        "To": USER_PHONE,
        "Body": message
    }
    response = requests.post(url, data=data, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
    
    if response.status_code == 201:
        print("SMS alert sent successfully!")
    else:
        print("Failed to send SMS:", response.text)

# Example Trigger
sensor_data = {"timestamp": "2025-02-05T12:00:01Z", "heartRate": 50, "respirationRate": 8}
send_sms_alert(sensor_data)
