from joystick import *
import json

class Globale:

    joystick_x = Joystick(0x4A,0,1000,500)# ads_i2c_adress,port,resolution send,dead_zone
    joystick_y = Joystick(0x4A,1,1000,500)# ads_i2c_adress,port,resolution send,dead_zone
    
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

    acces_send_data=0

    hoverboard_feed_back = {
    "cmd1" : 0,
    "cmd2" : 0,
    "speedR_meas" : 0,
    "speedL_meas" : 0,
    "batVoltage" : 0,
    "boardTemp" : 0,
    "Temperature" : 0,
    "cmdLed" : 0,
    "Roll" : 0,
    "Pitch" : 0
    }

    def data_to_send():

        checksum =0
        
        if not Globale.acces_send_data:
            return json.dumps({"mode":"pause"})

        if Globale.mode_hammer_robot :

            P=0
            I=0
            D=0

            for var in ["1000","100","10","1"]:
                P = P*10+Globale.P[var]
            for var in ["1000","100","10","1"]:
                I = I*10+Globale.I[var]
            for var in ["1000","100","10","1"]:
                D = D*10+Globale.D[var]

            coef_speed = Globale.coef_hammer["speed_10"]*10+Globale.coef_hammer["speed_1"]
            coef_steer = Globale.coef_hammer["steer_10"]*10+Globale.coef_hammer["steer_1"]

            pid = {
            "P" : P,
            "I" : I,
            "D" : D
            }

            mode = {
            "hammer" : 1,
            "pid" : pid,
            "coef_speed" : coef_speed,
            "coef_steer" : coef_steer
            }

            for key,value in pid.items():
                checksum += value

        else :

            coef_speed = Globale.coef_normal["speed_10"]*10+Globale.coef_normal["speed_1"]
            coef_steer = Globale.coef_normal["steer_10"]*10+Globale.coef_normal["steer_1"]

            mode = {
            "hammer" : 0,
            "coef_speed" : coef_speed,
            "coef_steer" : coef_steer
            }
        

        checksum += coef_speed+coef_steer
        checksum += Globale.speed_value+Globale.steer_value
       
        btn = {"A": Globale.button_state["A"],
                "B": Globale.button_state["B"],
                "X": Globale.button_state["X"],
                "Y": Globale.button_state["Y"],
                }
                
        for key,value in btn.items():
            checksum += value

        data = {"speed": Globale.speed_value,
                "steer": Globale.steer_value,
                "btn": btn,
                "mode": mode,
                "checksum": checksum,
                }
                
        return json.dumps(data)
                      
    def parse_feedback(str_feedback):
        try:
            str_feedback=json.loads(str_feedback.decode("utf-8")) 
        except Exception as e:
            print("\033[91m"+"str_feedback error "+str(e)+"\033[0m")

        #print("str_feedback",str_feedback)
        
        feedback_item = ["cmd1","cmd2","speedR_meas","speedL_meas","batVoltage","boardTemp","Temperature","cmdLed","Roll","Pitch"]
        
        for element in feedback_item:
            try:
                Globale.hoverboard_feed_back[element]=str_feedback[element]
            except KeyError :
                Globale.hoverboard_feed_back[element]="false"
            except Exception as e:
                print("\033[91m"+"str_feedback error "+str(e)+"\033[0m")

        
        #print("Globale.hoverboard_feed_back:",Globale.hoverboard_feed_back)
        
