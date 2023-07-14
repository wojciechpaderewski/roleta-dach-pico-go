import network
import time
import machine
from machine import Pin
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Moria","Barahir6")
time.sleep(5)
print(wlan.isconnected())

sensor = Pin(16, Pin.IN)

mqtt_server = '192.168.0.169'
port = 1883 
user = 'mqtt-usr'
password = '1369'
client_id = 'home_assistant'
sub_topic = b'/pokoj-wojtka/roleta-dach'
topic_msg = b'Movement Detected'

def callback(topic, msg):
    if(topic == sub_topic):
        print(msg)

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port, user, password, keepalive=3600)
    client.set_callback(callback)
    client.connect()
    client.subscribe(sub_topic)
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()


try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    if sensor.value() == 0:
        client.subscribe(sub_topic)
    else:
        pass