from joystick import *
import json

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

    mode_hammer_robot = 0 # 0=normal 1=hammer

    speed_value = 0
    speed_percentage=0
    steer_value =0
    steer_percentage=0

    def data_to_send():

        for i in Globale.button_state:
            total_value_dict =+ Globale.button_state[i]

        if Globale.mode_hammer_robot :

            for i in Globale.P:
                total_value_dict =+ Globale.P[i]
            for i in Globale.I:
                total_value_dict =+ Globale.I[i]
            for i in Globale.D:
                total_value_dict =+ Globale.D[i]
            for i in Globale.coef_hammer:
                total_value_dict =+ Globale.coef_hammer[i]

            pid = {
            "P" : Globale.P,
            "I" : Globale.I,
            "D" : Globale.D
            }

            mode = {
            "hammer" : 1,
            "pid" : pid,
            "coef" : Globale.coef_hammer
            }

        else :

            for i in Globale.coef_normal:
                total_value_dict =+ Globale.coef_normal[i]

            mode = {
            "hammer" : 0,
            "coef" : Globale.coef_normal
            }
            
        checksum = Globale.speed_value+Globale.steer_value+total_value_dict

        data = {"speed": Globale.speed_value,
                "steer": Globale.steer_value,
                "btn": Globale.button_state,
                "mode": Globale.button_state,
                "checksum": checksum,
                }
        return json.dumps(data)