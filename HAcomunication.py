import network
import time
import control
import machine
from umqtt.simple import MQTTClient

mqtt_server = '192.168.0.169'
port = 1883 
user = 'mqtt-usr'
password = '1369'
client_id = 'home_assistant'
pingIntervalTime = 20000

lastDistance = 0
bufferForInertion = 4
lastMillis = 0

set_topic = b'wojt-room/cover/roof/set'
state_topic = b'wojt-room/cover/roof/state'
set_position_topic = b'wojt-room/cover/roof/set_position'
position_topic = b'wojt-room/cover/roof/position'

lastState = b''
lastPosition = b''

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port, user, password, keepalive=60)
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
        print('Received %s on topic %s'%(msg, topic))
        onSetPositionTopic(msg)

def onSetTopic(msg):
    if msg == b'OPEN':
        client.publish(state_topic, 'opening')
        control.moveToGoal(control.maxEncoderValue)
    elif msg == b'CLOSE':
        client.publish(state_topic, 'closing')
        control.moveToGoal(0)
    elif msg == b'STOP':
        client.publish(state_topic, 'stopped')
        control.stop()
        control.setState('ready')
        print('Cover stopped')
    else :
        print('Unknown command %s'%(msg))
        control.stop()

def onSetPositionTopic(msg):
    value = int(msg)
    print('Moving to position %s'%(str(value)))
    control.moveToGoal(int(value))

def init():
    global client
    global wlan

    print('Connecting to MQTT Broker...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Moria","Barahir6")
    time.sleep(5)
    client = mqtt_connect()
    client.subscribe(set_topic)
    client.subscribe(set_position_topic)
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()


def publishState():
    global lastState
    
    if control.goal - bufferForInertion > control.getDistance() and lastState != 'opening' and lastState != 'open':
        client.publish(state_topic, 'opening')
        lastState = 'opening'
    elif control.goal + bufferForInertion < control.getDistance() and lastState != 'closing' and lastState != 'closed':
        client.publish(state_topic, 'closing')
        lastState = 'closing'

    if control.goal - bufferForInertion < control.getDistance() < control.goal + bufferForInertion and lastState != 'stopped':
        client.publish(state_topic, 'stopped')
        lastState = 'stopped'
        
    if (not control.getEndstopValue() or control.getDistance() <= 0) and lastState != 'closed':
        client.publish(state_topic, 'closed')
        lastState = 'closed'
    elif control.getDistance() >= control.maxEncoderValue and lastState != 'open':
        client.publish(state_topic, 'open')
        lastState = 'open'

def publishPosition():
    global lastPosition

    currentDistance = str(int(control.getDistance()))
    if lastPosition != currentDistance:
        client.publish(position_topic, currentDistance)
        lastPosition = currentDistance

def pingBroker():
    global lastMillis
    if control.milis() - lastMillis > pingIntervalTime:
        client.ping()
        lastMillis = control.milis()

def update():
    if control.isHommed == False:
        return

    client.check_msg()
    publishState()
    publishPosition()
    pingBroker()
