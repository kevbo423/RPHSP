#!/usr/bin/env python

# Imports for Original Security System
import RPi.GPIO as GPIO
import time
import sys
import signal
import os
import pygame

# Imports for LCD Screen
import i2c_driver
import time

# Global Variables
alarmSoundLocation = "/home/pi/RPHSP/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Set LCD Settings
mylcd = i2c_driver.LCD()

# Door Sensor class
class doorSensor:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.status = "null"
        self.currentState = True
        self.previousState = True

    def display_output(self):
        print(self.name + " Status: " + self.status)

    def get_string(self):
        doorSensorString = self.name + ":" + self.status
        print(doorSensorString)
        return doorSensorString

# Create array of sensors
sensors = []
sensors.append(doorSensor("Front Door", 16))
sensors.append(doorSensor("Living Room Window", 26))
sensors.append(doorSensor("Garage Door", 20))
sensors.append(doorSensor("Basement Door", 21))

# Set up the door sensor pins.
for sensor in sensors:
    GPIO.setup(sensor.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Main Function
try:
    os.system('clear')

    while True:

        # Variables
        securityBreach = False

        # Check each sensor for a security breach
        for sensor in sensors:
            sensor.currentState = GPIO.input(sensor.pin)
            if (sensor.currentState):
                # This means the door/window is open
                securityBreach = True
                print(sensor.name + " : !!!OPEN!!!")
            else:
                print(sensor.name + " : CLOSED")

        if (securityBreach):
            if (not pygame.mixer.music.get_busy()):
                pygame.mixer.music.load(alarmSoundLocation)
                pygame.mixer.music.play(-1)
        else:
            if (pygame.mixer.music.get_busy()):
                pygame.mixer.music.stop()

        # Time delay
        time.sleep(2)
        #os.system('clear')

except KeyboardInterrupt:
    mylcd.lcd_clear()
    print("Goodbye")
