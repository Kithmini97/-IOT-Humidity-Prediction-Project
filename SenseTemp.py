# Import essential packages.

import time

import Adafruit_DHT #Module necassarily needed to use DHT sensor.

import RPi.GPIO as GPIO #Module used to manipulate general purpose input and output.
GPIO.setmode(GPIO.BCM)

# Function to sense temperature through DHT11
def observeTemp(sensor, pin):
    
    print("------------Starting to read temperature--------------")
    # Pass the type of sensor and respective pin of sensor connected to raspberyy pi.
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is None and temperature is None:
        humidity, temperature = None
    else:
        humidity = round(humidity,2)
        temperature = round(temperature,2)
        F_temperatiure = (temperature *9/5 ) + 32
        heat_index = -42.379 + 2.04901523* F_temperatiure + 10.14333127*humidity - .22475541*F_temperatiure*humidity - .00683783*F_temperatiure*F_temperatiure - .05481717*humidity*humidity + .00122874*F_temperatiure*F_temperatiure*humidity + .00085282*F_temperatiure*humidity*humidity - .00000199*F_temperatiure*F_temperatiure*humidity*humidity

        
    return humidity,temperature,heat_index