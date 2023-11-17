import random
from paho.mqtt import client as mqtt_client
import json
import random
import time
from azure.storage.blob import AppendBlobService
import os

broker = '34.88.147.32'
port = 1883
topic = "gc/traffic/prod/mrf/257017920/#"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'skyss'
password = 'e2dye9ZRoJZn8t_wNzuq'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def append_data_to_blob(data, data1):
  service = AppendBlobService(account_name="skyssndpstorageaccount", 
            account_key="P37ctI6HGBdqDepa+fqEn/fiN0r3Kff01sXFUSofU7uNSGgpVOW5MuRYZYo1IDv7zoPfHpKOhh82+AStjps59w==")
  json_data = json.dumps(data1)
  data = json.dumps(data1)
  print(data1)
  try:
    service.append_blob_from_text(container_name="rawmqttdata", blob_name="test3.json", text = data + "\n")
  except:
    service.create_blob(container_name="rawmqttdata", blob_name="test3.json")
    service.append_blob_from_text(container_name="rawmqttdata", blob_name="test3.json", text = data + "\n")
  print('Data Appended to Blob Successfully.')

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(msg.payload.decode())
        append_data_to_blob("data", json.loads(msg.payload.decode()))
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()

