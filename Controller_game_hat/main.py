import RPi.GPIO as GPIO
import threading

from tkinter_game_hat import *
from globales import *
from Config.config import *
    
def interrupt_pin(channel):
    
     #Callback fonction for each button and joystick
     
    for key,value in Globale.BUTTON_PIN.items():
        if channel == value :
            print("BUTTON_PIN : ",key)
    if GPIO.input(channel):       
        print ("Rising edge detected on ",channel)
    else:                  
        print ("Falling edge detected on ",channel)
        
        if channel == Globale.BUTTON_PIN["START"] :
            Globale.acces_send_data=0
            lcd.print_menu_start()
        elif channel == Globale.BUTTON_PIN["SELECT"] :
            lcd.select()
        elif channel == Globale.BUTTON_PIN["R1"] :
            lcd.manage_L1_R1(-1)
        elif channel == Globale.BUTTON_PIN["L1"] :
            lcd.manage_L1_R1(1)
        elif channel == Globale.JOYSTICK_PIN["UP"] :
            lcd.manage_up_down(-1)
        elif channel == Globale.JOYSTICK_PIN["DOWN"] :
            lcd.manage_up_down(1)
        elif channel == Globale.JOYSTICK_PIN["RIGHT"] :
            lcd.manage_left_right(1)
        elif channel == Globale.JOYSTICK_PIN["LEFT"] :
            lcd.manage_left_right(-1)

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

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

def setup():
    try :
        load_param()
    except:
        print("Erreur load_param")
        
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    
    # Create interrupt event for each button and joystick
    
    for key,value in Globale.BUTTON_PIN.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(value, GPIO.BOTH, callback=interrupt_pin, bouncetime=175)
            
    for key,value in Globale.JOYSTICK_PIN.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(value, GPIO.BOTH, callback=interrupt_pin, bouncetime=75)

def loop():

    while True:
        read_button()
        read_joystick()
        lcd.update()
        lcd.manage_mode()

        
if __name__ == "__main__":
    
    setup()
    
    root = tk.Tk()
    root.title("Controller robot")
    root.tk.call("source", "/home/pi/Desktop/Sun-Valley-ttk-theme-master/sun-valley.tcl")
    root.tk.call("set_theme", "dark")
    root.attributes('-fullscreen', True) #1280x720
    root.config(cursor="none")
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
    
    Bluetooth_rpi.cleanup
    


