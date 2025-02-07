# web dashboard with plotly
# pip install dash paho-mqtt numpy
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import paho.mqtt.client as mqtt
import numpy as np

app = dash.Dash(__name__)

# Live Data Buffer
data_buffer = []

# MQTT Setup
MQTT_BROKER = "192.168.1.100"
MQTT_TOPIC = "sensor/mmwave"

def on_message(client, userdata, message):
    global data_buffer
    value = float(message.payload.decode())
    data_buffer.append(value)
    if len(data_buffer) > 500:
        data_buffer.pop(0)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

app.layout = html.Div([
    html.H1("Real-Time mmWave Sensor Data"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)  # Updates every second
])

@app.callback(Output('live-graph', 'figure'), Input('interval', 'n_intervals'))
def update_graph(n):
    global data_buffer
    return {"data": [{"y": data_buffer, "type": "line", "name": "Sensor Data"}]}

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
