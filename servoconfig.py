import os
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
# import file to read temperature
from SenseTemp import observeTemp

GPIO.setmode(GPIO.BCM)
servo_pin = 17

GPIO.setup(servo_pin, GPIO.OUT)
sensor = Adafruit_DHT.DHT22   # Type of sensor used
temp_pin = 4    
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)



def set_angle(heat_index):
    angle = 0# humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)  # Get the reading from the sensors
    humidity, temperature, heat_index  = observeTemp(sensor, temp_pin)
    print("set angle function called")
    angle = 0
    if heat_index < 120:
        angle = 30
    elif heat_index < 121:
        angle = 45
    elif heat_index < 121.5:
        angle = 90
    elif heat_index < 122:
        angle = 160
    else:
        angle = 170

    duty = angle / 18 + 2.5
    pwm.ChangeDutyCycle(duty)

# while True:
# 	humidity, temperature,heat_index = observeTemp(sensor,temp_pin)
# 	set_angle(heat_index)
# 	time.sleep(3)

def run_motor(heat_index):
    print("run motor function called")
    set_angle(heat_index)
