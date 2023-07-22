
# Import necassary modules
import time
import paho.mqtt.client as paho # Client used in connecting to an MQTT Broker.
from paho import mqtt

# Checking for publisher-subscriber connectivity through callback event.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# Print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Check connection success.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode('utf-8')))

#-------Defining the mqtt broker with access port.
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883

#--------Defining the MQTT topic to publish data and subscribe from it.
mqtt_topic = "Group11/Temperature"

#----------------------------------------------------------------------------------------------

#Define the MQTT client.
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# connect to HiveMQ
client.connect(mqtt_broker, mqtt_port)

# setting callbacks to subscribe.
client.on_subscribe = on_subscribe
client.on_message = on_message

#----------------------------------------------------------------------------------------------

#subscribe to the relevant topic
client.subscribe(mqtt_topic, qos=1)

#loop the process.
client.loop_forever()