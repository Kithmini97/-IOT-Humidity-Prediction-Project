# Import necessary modules
import json
import time
import paho.mqtt.client as paho # Client used in connecting to an MQTT Broker.
from paho import mqtt
import Adafruit_DHT # Module necessarily needed to use DHT sensor.
import RPi.GPIO as GPIO # Module used to manipulate general purpose input and output


from servoconfig import run_motor
from SenseTemp import observeTemp #Import function to sense environment temperature.

GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.DHT11 # Initializing the sensor.
pin = 4 # GPIO pin 4 of raspberry pi is connected with sensor.
sensor_data = {'temperature' : 0, 'humidity' : 0} # The sensor data received is saved as a dictionary.

# -------------------------------------------------- INITIATING A SELF HOSTED MQTT MANAGEMENT ------------------------------------------------

# Setting callback for events to check connection.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# Setting callback to check if publisher is working.
def on_publish(client, userdata, mid, properties=None):
    print("Published mid: " + str(mid))

# ----------------------------------------------------------------------------------------------
mqtt_broker = "broker.hivemq.com"  # Defining the self-hosted broker used.
mqtt_port = 1883 # Mqtt broker access port.

mqtt_topic = "Group48/data" # Defining the MQTT topic used.

# ----------------------------------------------------------------------------------------------

# Instantiate the client with parameters.
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5) # Defining the paho client.
client.on_connect = on_connect

# connect the client to HiveMQ
client.connect(mqtt_broker, mqtt_port)

# Setting callback on publishing.
client.on_publish = on_publish

client.loop_start()

# ----------------------------------------------------------------------------------------------

# Publish
# ----------------------------------------------------------------------------------------------
while True:
    humidity, temperature, heat_index = observeTemp(sensor, pin) # call the imported function defined.
    if humidity is None and temperature is None:
        print("Failed to get reading. Try Again")
    else:
        run_motor(heat_index) 
        # data={"temperature" :temperature , "humidity" : humidity}
        # payload = json.dumps({"temperature":temperature, "humidity" : humidity})
        # client.publish(mqtt_topic+"/data", payload=payload, qos=1)
        # print("Temperature={0:0.1f}*C Humidity={1:0.2f}%".format(temperature,humidity)) # Obtaining the sensed temperature.
        F_temperatiure = (temperature *9/5 ) + 32
        heat_index = -42.379 + 2.04901523* F_temperatiure + 10.14333127*humidity - .22475541*F_temperatiure*humidity - .00683783*F_temperatiure*F_temperatiure - .05481717*humidity*humidity + .00122874*F_temperatiure*F_temperatiure*humidity + .00085282*F_temperatiure*humidity*humidity - .00000199*F_temperatiure*F_temperatiure*humidity*humidity
        print("Temperature={0:0.1f}*C Humidity={1:0.2f}% Heat Index={2:0.2f}".format(temperature, humidity, heat_index))
        client.publish(mqtt_topic+"/temperature", payload=str(temperature), qos=1)
        client.publish(mqtt_topic+"/humidity", payload=str(humidity), qos=1)
        client.publish(mqtt_topic+"/heat_index", payload="{0:0.1f}".format(heat_index), qos=1)
        
        
    time.sleep(0.1)


# Client loop stops only when done manually.
# client.loop_forever()
