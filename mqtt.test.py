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
pos_sub = b'wojt-room/cover/roof/set_position'
pos_pub = b'wojt-room/cover/roof/position'

topic_msg = 'closed'

def callback(topic, msg):
    global topic_msg
    print((topic, msg))
    if(topic == sub_topic):
        topic_msg = setState(msg)
        time.sleep(3)
        client.publish(pub_topic, topic_msg)
    if(topic == pos_sub):
        print(msg)
        sub_topicmsg = '100'
        time.sleep(3)
        client.publish(pos_pub, sub_topicmsg)
    

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port, user, password, keepalive=3600)
    client.set_callback(callback)
    client.connect()
    client.subscribe(sub_topic)
    client.subscribe(pos_sub)
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
except OSError as e:
    reconnect()
while True:
    if sensor.value() == 0:
        client.check_msg()
    else:
        pass