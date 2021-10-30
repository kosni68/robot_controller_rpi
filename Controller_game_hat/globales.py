from joystick import *

class Globale:

    joystick_x = Joystick(0x4A,0,0x7FFF,500)# ads_i2c_adress,port,resolution send,dead_zone
    joystick_y = Joystick(0x4A,1,0x7FFF,500)# ads_i2c_adress,port,resolution send,dead_zone
    
    JOYSTICK_PIN = {
    "UP" : 5,
    "DOWN" : 6,
    "LEFT" : 13,
    "RIGHT" : 19
    }

    BUTTON_PIN = {
    "A" : 26,
    "B" : 12,
    "X" : 16,
    "Y" : 20,
    "START" : 21,
    "SELECT" : 4,
    "R1" : 18,
    "L1" : 23
    }
    
    joystick_current_value = {
    "X" : 512,
    "Y" : 512
    }
    
    joystick_current_value = {
    "X" : 512,
    "Y" : 512
    }
    
    button_state = {
    "A" : 0,
    "B" : 0,
    "X" : 0,
    "Y" : 0,
    "START" : 0,
    "SELECT" : 0,
    "R1" : 0,
    "L1" : 0
    }
        
    inverse = {
    "direction_speed" : 0,
    "direction_steer" : 0,
    "steer_speed" : 0
    }

    P = {
    "1000" : 0,
    "100" : 0,
    "10" : 0,
    "1" : 0
    }

    I = {
    "1000" : 0,
    "100" : 0,
    "10" : 0,
    "1" : 0
    }

    D = {
    "1000" : 0,
    "100" : 0,
    "10" : 0,
    "1" : 0
    }

    coef_normal = {
    "speed_10" : 0,
    "speed_1" : 0,
    "steer_10" : 0,
    "steer_1" : 0
    }

    coef_hammer = {
    "speed_10" : 0,
    "speed_1" : 0,
    "steer_10" : 0,
    "steer_1" : 0
    }

    mode_robot = 0 # 0=normal 1=hammer

    speed_value = 0
    speed_percentage=0
    steer_value =0
    steer_percentage=0