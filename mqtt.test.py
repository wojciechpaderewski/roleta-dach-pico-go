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
sub_topic = b'wojt-room/cover/roof/set'
pub_topic = b'wojt-room/cover/roof/state'

topic_msg = 'unknown'

def callback(topic, msg):
    print('callback')
    global topic_msg
    print(setState(msg))
    if(topic == sub_topic):
        topic_msg = setState(msg)
    

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


def setState(msg):
    if msg == b'OPEN':

        return 'open'
    elif msg == b'CLOSE':

        return 'closed'
    else:

        return 'unknown'

try:
    client = mqtt_connect()
    client.subscribe(sub_topic)
except OSError as e:
    reconnect()
while True:
    if sensor.value() == 0:
        client.check_msg()
        if(topic_msg != 'unknown'):
            time.sleep(2)
            client.publish(pub_topic, topic_msg)
    else:
        pass