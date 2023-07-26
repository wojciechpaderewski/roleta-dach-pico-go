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

lastDistance = 0

set_topic = b'wojt-room/cover/roof/set'
state_topic = b'wojt-room/cover/roof/state'
set_position_topic = b'wojt-room/cover/roof/set_position'
position_topic = b'wojt-room/cover/roof/position'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port, user, password, keepalive=3600)
    client.set_callback(callback)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def callback(topic, msg):
    global topic_msg
    if(topic == set_topic):
        print('Received %s on topic %s'%(msg, topic))
        onSetTopic(msg)
    if(topic == set_position_topic):
        global lastMsg
        print('Received %s on topic %s'%(msg, topic))
        lastMsg = msg
        onSetPositionTopic(msg)

def onSetTopic(msg):
    if msg == b'OPEN':
        print('Opening cover')
        client.publish(state_topic, 'opening')
        control.openCover()
        client.publish(state_topic, 'open')
        print('Cover opened')
    elif msg == b'CLOSE':
        print('Closing cover')
        client.publish(state_topic, 'closing')
        control.closeCover()
        client.publish(state_topic, 'closed')
        print('Cover closed')
    elif msg == b'STOP':
        print('Stopping cover')
        client.publish(state_topic, 'stopped')
        control.stop()
        print('Cover stopped')
    else :
        print('Unknown command %s'%(msg))
        control.stop()

def onSetPositionTopic(msg):
    print('Moving to position %s'%(msg))
    control.moveToPosition(int(msg))
    print('Moved to position %s'%(msg))


def reconnect():
    while not wlan.isconnected():
        print('Failed to connect to the MQTT Broker. Reconnecting...')
        time.sleep(5)
        mqtt_connect()

def init():
    print('init')
    global client
    global wlan

    print('Connecting to MQTT Broker...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Moria","Barahir6")
    client = mqtt_connect()
    client.subscribe(set_topic)
    client.subscribe(set_position_topic)
    return True


def update():
    global lastDistance
    client.check_msg()
    if lastDistance != control.getDistance():
        client.publish(position_topic, control.getDistance())
        lastDistance = control.getDistance()
