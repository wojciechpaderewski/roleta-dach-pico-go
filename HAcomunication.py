import network
import time
import control
from machine import Pin
from umqtt.simple import MQTTClient

mqtt_server = '192.168.0.169'
port = 1883 
user = 'mqtt-usr'
password = '1369'
client_id = 'home_assistant'

set_topic = b'wojt-room/cover/roof/set'
state_topic = b'wojt-room/cover/roof/state'
set_position_topic = b'wojt-room/cover/roof/set_position'
position_topic = b'wojt-room/cover/roof/position'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Moria","Barahir6")
time.sleep(5)
print(wlan.isconnected())

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port, user, password, keepalive=3600)
    client.set_callback(callback)
    client.connect()
    client.subscribe(set_topic)
    client.subscribe(set_position_topic)
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def callback(topic, msg):
    global topic_msg
    if(topic == set_topic):
        onSetTopic(msg)
    if(topic == set_position_topic):
        onSetPositionTopic(msg)

def onSetTopic(msg):
    if msg == b'OPEN':
        client.publish(state_topic, 'opening')
        control.openCover()
        client.publish(state_topic, 'open')
    elif msg == b'CLOSE':
        client.publish(state_topic, 'closing')
        control.closeCover()
        client.publish(state_topic, 'closed')

def onSetPositionTopic(msg):
    control.moveToPosition(int(msg))
    encoderValue = control.getDistance()
    client.publish(position_topic, encoderValue)

def reconnect():
    while not wlan.isconnected():
        print('Failed to connect to the MQTT Broker. Reconnecting...')
        time.sleep(5)
        mqtt_connect()

def init():
    global client
    try:
        client = mqtt_connect()
    except OSError as e:
        reconnect()

def update():
    client.check_msg()
