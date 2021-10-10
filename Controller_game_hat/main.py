import RPi.GPIO as GPIO
import threading
import time
import json

from joystick import *
from tkinter_game_hat import *
from globales import *

joystick_x = Joystick(0x4A,0,0x7FFF,500)# ads_i2c_adress,port,resolution send,dead_zone
joystick_y = Joystick(0x4A,1,0x7FFF,500)# ads_i2c_adress,port,resolution send,dead_zone

def save_param():
    struct_config = {"joystick_x": {"max_value": joystick_x.max_value,
                                    "middle_value": joystick_x.middle_value,
                                    "min_value": joystick_x.min_value
                                    },
                     "joystick_y": {"max_value": joystick_x.max_value,
                                    "middle_value": joystick_x.middle_value,
                                    "min_value": joystick_x.min_value
                                    },
                     "param": {"inverse": Globale.inverse
                            },
                }

    with open('controller_config.json', 'w') as file:
        json.dump(struct_config, file)

def load_param():
    with open('controller_config.json', 'r') as file:
        datadict = json.load(file)
        
    joystick_x.max_value=datadict["joystick_x"]["max_value"]
    joystick_x.middle_value=datadict["joystick_x"]["middle_value"]
    joystick_x.min_value=datadict["joystick_x"]["min_value"]
    
    joystick_y.max_value=datadict["joystick_y"]["max_value"]
    joystick_y.middle_value=datadict["joystick_y"]["middle_value"]
    joystick_y.min_value=datadict["joystick_y"]["min_value"]
    
    Globale.inverse=datadict["param"]["inverse"]

def setup():
    load_param()
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    
    # Create interrupt event for each button and joystick
    
    for item in Globale.BUTTON_PIN.items():
        print("item : ",item[1])
        GPIO.setup(item[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(item[1], GPIO.BOTH, callback=interrupt_pin, bouncetime=75)
            
    for item in Globale.JOYSTICK_PIN.items():
        print("item : ",item[1])
        GPIO.setup(item[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(item[1], GPIO.BOTH, callback=interrupt_pin, bouncetime=75)
    
def interrupt_pin(channel):
    
     #Callback fonction for each button and joystick
     
    for item in Globale.BUTTON_PIN.items():
        if channel == item[1] :
            print("BUTTON_PIN : ",item[0])
    if GPIO.input(channel):       
        print ("Rising edge detected on ",channel)
    else:                  
        print ("Falling edge detected on ",channel)
        
        if channel == Globale.BUTTON_PIN["START"] :
            lcd.menu_start(1,0)
        elif channel == Globale.BUTTON_PIN["SELECT"] :            
            lcd.select();
        elif channel == Globale.JOYSTICK_PIN["UP"] :
            if lcd.page[0] == "menu":
                lcd.menu_start(0,-1)
        elif channel == Globale.JOYSTICK_PIN["DOWN"] :
            if lcd.page[0] == "menu":
                lcd.menu_start(0,1)

def loop():
    while True:
        
        for item in Globale.BUTTON_PIN.items():
            if GPIO.input(item[1]) == True:
                Globale.button_state[item[0]]=0
            else:
                Globale.button_state[item[0]]=1
                
        if Globale.inverse["steer_speed"]:
            speed_value = joystick_x.scale_current_value(Globale.inverse["direction_speed"])
            steer_value = joystick_y.scale_current_value(Globale.inverse["direction_steer"])
        else:
            speed_value = joystick_y.scale_current_value(Globale.inverse["direction_speed"])
            steer_value = joystick_x.scale_current_value(Globale.inverse["direction_steer"])
                
        lcd.joy_steer.set(value="Steer = "+str(steer_value))
        lcd.joy_speed.set(value="Speed = "+str(speed_value))
        lcd.joy_real_x.set(value="X = "+str(joystick_x.current_read_value))
        lcd.joy_real_y.set(value="Y = "+str(joystick_y.current_read_value))
        lcd.device_data.set(value=Bluetooth_rpi.data)
        
        if lcd.page[0] == "cal_auto":
                    if lcd.page[1] == "no_move_x":
                        joystick_x.calibration_middle_joystick(3,lcd.compteur_str.set)
                        lcd.calibration_auto("no_move_y")
                    if lcd.page[1] == "no_move_y":
                        joystick_y.calibration_middle_joystick(3,lcd.compteur_str.set)
                        lcd.calibration_auto("move_x")
                    if lcd.page[1] == "move_x":
                        joystick_x.calibration_max_min_joystick(7,lcd.compteur_str.set)
                        lcd.calibration_auto("move_y")
                    elif lcd.page[1] == "move_y":
                        joystick_y.calibration_max_min_joystick(7,lcd.compteur_str.set)
                        lcd.calibration_result(joystick_x.min_value,joystick_x.middle_value,joystick_x.max_value,joystick_y.min_value,joystick_y.middle_value,joystick_y.max_value)
                        save_param()
        
    

if __name__ == "__main__":
    
    setup()
    
    root = tk.Tk()
    root.title("Controller robot")
    root.tk.call("source", "/home/pi/Desktop/Sun-Valley-ttk-theme-master/sun-valley.tcl")
    root.tk.call("set_theme", "dark")
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.destroy())
    
    lcd = App(root)
    lcd.pack(fill="both", expand=True)
      
    th1 = threading.Thread(target=loop)
    th2 = threading.Thread(target=Bluetooth_rpi.run_server)
    th3 = threading.Thread(target=Bluetooth_rpi.run_client)
    
    th1.start()
    th2.start()
    th3.start()
    
    root.mainloop()
    
    th1.join()
    th2.join()
    th3.join()
    
    Bluetooth_rpi.device.cleanup
    


