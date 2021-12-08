from globales import *
import RPi.GPIO as GPIO
from tkinter_game_hat import *

from print_debug import *
pin_print = print_debug("PIN",36)

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
   
def setup_pin():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

def read_button():
    # Read button state
    for key,value in Globale.BUTTON_PIN.items():
        if GPIO.input(value) == True:
            Globale.button_state[key]=0
        else:
            Globale.button_state[key]=1

def read_joystick():
    # Read joystick value
    if Globale.inverse["steer_speed"]:
        Globale.speed_value = Globale.joystick_x.scale_current_value(Globale.inverse["direction_speed"])
        Globale.speed_percentage = _map(Globale.speed_value,-Globale.joystick_x.resolution,Globale.joystick_x.resolution,-100,100)
        Globale.steer_value = Globale.joystick_y.scale_current_value(Globale.inverse["direction_steer"])
        Globale.steer_percentage = _map(Globale.steer_value,-Globale.joystick_x.resolution,Globale.joystick_y.resolution,-100,100)
    else:
        Globale.speed_value = Globale.joystick_y.scale_current_value(Globale.inverse["direction_speed"])
        Globale.speed_percentage = _map(Globale.speed_value,-Globale.joystick_x.resolution,Globale.joystick_y.resolution,-100,100)
        Globale.steer_value = Globale.joystick_x.scale_current_value(Globale.inverse["direction_steer"])
        Globale.steer_percentage = _map(Globale.steer_value,-Globale.joystick_x.resolution,Globale.joystick_x.resolution,-100,100)
