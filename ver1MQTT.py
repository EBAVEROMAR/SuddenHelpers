#sudo apt update
# sudo apt install mosquitto mosquitto-clients
# mosquitto -v
# pip install paho-mqtt numpy scipy matplotlib
#

import paho.mqtt.client as mqtt
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

data_buffer = []

# MQTT Config
MQTT_BROKER = "192.168.1.100"  # Replace with your broker IP
MQTT_TOPIC = "sensor/mmwave"

def on_message(client, userdata, message):
    global data_buffer
    try:
        value = float(message.payload.decode())  # Convert sensor output to float
        data_buffer.append(value)
        if len(data_buffer) > 500:  # Process every 500 samples
            process_signal()
    except Exception as e:
        print("Error:", e)

def process_signal():
    global data_buffer
    time = np.linspace(0, len(data_buffer), len(data_buffer))
    
    # Apply FFT
    fft_values = np.fft.fft(data_buffer)
    freqs = np.fft.fftfreq(len(data_buffer))

    # Detect peaks for breathing (~0.2-0.5 Hz) and heart rate (~1-2 Hz)
    breath_peak = freqs[np.argmax(np.abs(fft_values[(freqs > 0.1) & (freqs < 0.5)]))]
    heart_peak = freqs[np.argmax(np.abs(fft_values[(freqs > 0.8) & (freqs < 2.0)]))]

    print(f"Breathing Rate: {breath_peak * 60:.2f} BPM, Heart Rate: {heart_peak * 60:.2f} BPM")

    # Plot data
    plt.figure(figsize=(10, 5))
    plt.plot(time, data_buffer, label="Raw Sensor Data")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Vital Sign Signal")
    plt.legend()
    plt.show()

    data_buffer = []  # Clear buffer

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
client.loop_forever()
