import sys
import threading

from tkinter_game_hat import *
from globales import *
from Config.config import *
from input import *

from print_debug import *
config_print = print_debug("CONFIG",35)
 
def create_interrupt_pin():
    # Create interrupt event for each button and joystick
    
    for key,value in Globale.BUTTON_PIN.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(value, GPIO.BOTH, callback=interrupt_pin, bouncetime=175)
            
    for key,value in Globale.JOYSTICK_PIN.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(value, GPIO.BOTH, callback=interrupt_pin, bouncetime=75)

def interrupt_pin(channel):
    
     #Callback fonction for each button and joystick
     
    for key,value in Globale.BUTTON_PIN.items():
        if channel == value :
            pin_print.info("BUTTON_PIN : ",key)
    if GPIO.input(channel):       
        pin_print.info("Rising edge detected on ",channel)
    else:                  
        pin_print.info("Falling edge detected on ",channel)
        
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

def setup():
    try :
        load_param()
        config_print.info("loading param sucess")
    except Exception as e:
        config_print.error("Error load_param",e)
        
    setup_pin()
    create_interrupt_pin()
    
def loop():

    while True:
        read_button()
        read_joystick()
        lcd.update()
        lcd.manage_mode()

def loop_send_message():
    while True:
        udp_client.sendMessage(Globale.data_to_send())

def loop_receive_message():
    while True:
        receive_msg=udp_client.receiveMessages()
        Globale.parse_feedback(receive_msg)

def main():
    
    setup()
    
    th1 = threading.Thread(target=loop)
    th2 = threading.Thread(target=loop_send_message)
    th3 = threading.Thread(target=loop_receive_message)

    th1.start()
    th2.start()
    th3.start()

    root.mainloop()
        
    th1.join()
    th2.join()
    th3.join()
    
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Controller robot")
    root.tk.call("source", "/home/pi/Desktop/Sun-Valley-ttk-theme-master/sun-valley.tcl")
    root.tk.call("set_theme", "dark")
    root.attributes('-fullscreen', True) #1280x720
    root.config(cursor="none")
    root.bind('<Escape>', lambda e: root.destroy())

    lcd = Tkinter_app(root)
    lcd.pack(fill="both", expand=True)

    udp_client=Udp_client()

    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    


