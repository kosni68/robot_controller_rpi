import tkinter as tk
from tkinter import ttk
from globales import *
from bluetooth_rpi_thread import *
from Config.config import *

class App(ttk.Frame):
    
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.bg_img = tk.PhotoImage(file="img/background2.png")
        self.btn_on = tk.PhotoImage(file="img/btn_on.png")
        self.btn_off = tk.PhotoImage(file="img/btn_off.png")
        self.switch_on = tk.PhotoImage(file="img/switch-on.png")
        self.switch_off = tk.PhotoImage(file="img/switch-off.png")

        self.position_menu = 0
        self.position_param =0
        self.position_v = 0
        self.position_h = 0
        self.size_title=50
        self.size_item=40


        # Create value lists
        self.page = ["",""]
        #self.page_list = ["menu", "controller","receiver","parametres","cal_auto"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_5 = tk.DoubleVar(value=75.0)
       
        
        self.coef_speed_normal = [tk.StringVar(value="0"),tk.StringVar(value="0")]
        self.coef_steer_normal = [tk.StringVar(value="0"),tk.StringVar(value="0")]

        self.coef_speed_hammer = [tk.StringVar(value="0"),tk.StringVar(value="0")]
        self.coef_steer_hammer = [tk.StringVar(value="0"),tk.StringVar(value="0")]

        self.joy_real_x = tk.StringVar(value="X = ")
        self.joy_real_y = tk.StringVar(value="Y = ")
        self.joy_speed = tk.StringVar(value="Speed = ")
        self.joy_steer = tk.StringVar(value="Steer = ")
        self.joy_speed_percent = tk.StringVar(value="")
        self.joy_steer_percent = tk.StringVar(value="")
        self.device_data = tk.StringVar(value=str(Bluetooth_rpi.data))
        
        # Compteur variables
        self.compteur = 5
        self.compteur_str = tk.IntVar(value=str(self.compteur))
        

        # Create widgets :
        #self.emetteur_widgets()
        #self.create_main_frame()
        self.menu_start()
     
    def overflow(self,limite,increment,value):
        value += increment
        if value <0:
            value = limite
        elif value >limite:
            value = 0
        
        return value

    def update(self):
        
        if self.page[0] == "controller":
            try :
                if Globale.button_state["A"] == True:self.label_A.configure(image=self.btn_on)
                else:self.label_A.configure(image=self.btn_off)
                if Globale.button_state["B"] == True:self.label_B.configure(image=self.btn_on)
                else:self.label_B.configure(image=self.btn_off)
                if Globale.button_state["X"] == True:self.label_X.configure(image=self.btn_on)
                else:self.label_X.configure(image=self.btn_off)
                if Globale.button_state["Y"] == True:self.label_Y.configure(image=self.btn_on)
                else:self.label_Y.configure(image=self.btn_off)
                if Globale.button_state["R1"] == True:self.label_R1.configure(image=self.btn_on)
                else:self.label_R1.configure(image=self.btn_off)
                if Globale.button_state["L1"] == True:self.label_L1.configure(image=self.btn_on)
                else:self.label_L1.configure(image=self.btn_off)
            except : 
                pass
                
                
            self.joy_steer.set(value="Steer = "+str(Globale.steer_value))
            self.joy_steer_percent.set(value=str(Globale.steer_percentage)+"%")
            self.joy_speed.set(value="Speed = "+str(Globale.speed_value))
            self.joy_speed_percent.set(value=str(Globale.speed_percentage)+"%")
            self.joy_real_x.set(value="X = "+str(Globale.joystick_x.current_read_value))
            self.joy_real_y.set(value="Y = "+str(Globale.joystick_y.current_read_value))
            self.device_data.set(value=Bluetooth_rpi.data)

    
        elif self.page[0] == "parametres":

            if self.page[1] == "normal":
                self.coef_speed_normal[0].set(value=str(Globale.coef_normal["speed_1"]))
                self.coef_speed_normal[1].set(value=str(Globale.coef_normal["speed_10"]))

                self.coef_steer_normal[0].set(value=str(Globale.coef_normal["steer_1"]))
                self.coef_steer_normal[1].set(value=str(Globale.coef_normal["steer_10"]))

            elif self.page[1] == "hammer":
                self.coef_speed_hammer[0].set(value=str(Globale.coef_hammer["speed_1"]))
                self.coef_speed_hammer[1].set(value=str(Globale.coef_hammer["speed_10"]))

                self.coef_steer_hammer[0].set(value=str(Globale.coef_hammer["steer_1"]))
                self.coef_steer_hammer[1].set(value=str(Globale.coef_hammer["steer_10"]))

    def create_main_frame(self):

        self.main_frame = ttk.Frame(self, padding=(20, 10))
        self.main_frame.pack(pady=20)
        
        # Create a main Fram        
        #self.label_bg = ttk.Label(self, image=self.bg_img)
        #self.label_bg.place(x=0, y=0)

        #self.main_frame = ttk.Frame(self, padding=(20, 10))
        #self.main_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
    def clear(self):
            
        try:    
            for widget in self.main_frame.winfo_children():
                widget.destroy()
                self.main_frame.destroy()
        except:
            pass

        try:    
            self.main_frame.destroy()
        except:
            pass

        try:    
            self.canvas.destroy()
        except:
            pass
        
    def select(self):
        if self.page[0] == "menu":
            self.clear()
            if self.position_menu ==0:
                self.controller_widgets()
            elif self.position_menu ==1:
                self.controller_widgets()
            elif self.position_menu ==2:
                self.recepteur_widgets()
            elif self.position_menu ==3:
                self.parametres_widgets()

        elif self.page[0] == "parametres":
            if self.page[1] == "joy":
                if self.position_param ==0:
                    Globale.inverse["direction_speed"]= not Globale.inverse["direction_speed"]
                    self.print_param_joy()
                    save_param()
                if self.position_param ==1:
                    Globale.inverse["direction_steer"]= not Globale.inverse["direction_steer"]
                    self.print_param_joy()
                    save_param()
                if self.position_param ==2:
                    Globale.inverse["steer_speed"]= not Globale.inverse["steer_speed"]
                    self.print_param_joy()
                    save_param()
                if self.position_param ==3:
                    self.compteur_str.set(value=3)
                    self.calibration_auto("no_move_x")
            
            elif self.page[1] == "normal":
                if self.position_v == 0 and self.position_h == 0 : 
                    Globale.coef_normal["speed_1"]+=1
                    Globale.coef_normal["speed_1"]=self.overflow(9,0,Globale.coef_normal["speed_1"])
                elif self.position_v == 0 and self.position_h == 1 : 
                    Globale.coef_normal["speed_10"]+=1
                    Globale.coef_normal["speed_10"]=self.overflow(9,0,Globale.coef_normal["speed_10"])
                elif self.position_v == 1 and self.position_h == 0 : 
                    Globale.coef_normal["steer_1"]+=1
                    Globale.coef_normal["steer_1"]=self.overflow(9,0,Globale.coef_normal["steer_1"])
                elif self.position_v == 1 and self.position_h == 1 : 
                    Globale.coef_normal["steer_10"]+=1
                    Globale.coef_normal["steer_10"]=self.overflow(9,0,Globale.coef_normal["steer_10"])
            
            elif self.page[1] == "hammer":
                if self.position_v == 0 and self.position_h == 0 : 
                    Globale.coef_hammer["speed_1"]+=1
                    Globale.coef_hammer["speed_1"]=self.overflow(9,0,Globale.coef_hammer["speed_1"])
                elif self.position_v == 0 and self.position_h == 1 : 
                    Globale.coef_hammer["speed_10"]+=1
                    Globale.coef_hammer["speed_10"]=self.overflow(9,0,Globale.coef_hammer["speed_10"])
                elif self.position_v == 1 and self.position_h == 0 : 
                    Globale.coef_hammer["steer_1"]+=1
                    Globale.coef_hammer["steer_1"]=self.overflow(9,0,Globale.coef_hammer["steer_1"])
                elif self.position_v == 1 and self.position_h == 1 : 
                    Globale.coef_hammer["steer_10"]+=1
                    Globale.coef_hammer["steer_10"]=self.overflow(9,0,Globale.coef_hammer["steer_10"])
            
                save_param()
              
    def controller_widgets(self):
        # Createcontroller_widgets
        self.page[0] = "controller"

        self.create_main_frame()

        self.joy_frame = tk.Frame(self.main_frame)
        self.joy_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Create a Frame joystick read
        
        self.labelwidget = ttk.Label(self.joy_frame, text="Joy read", font=("-size", self.size_title,"-weight", "bold"))
        
        self.label_frame = tk.LabelFrame(self.joy_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
                
        self.label = ttk.Label(
            self.label_frame,
            textvariable=self.joy_real_x,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=10,
        )
        self.label.pack(ipadx=0, ipady=10)
        
        self.label = ttk.Label(
            self.label_frame,
            textvariable=self.joy_real_y,
            justify="left",
            font=("-size", self.size_item, "-weight", "bold"),
            width=10,
        )
        self.label.pack(ipadx=0, ipady=10)
        
        # Create a Frame joystick send
        
        self.labelwidget = ttk.Label(self.joy_frame, text="Joy send",  font=("-size", self.size_title,"-weight", "bold"),)
        
        self.label_frame = tk.LabelFrame(self.joy_frame, labelwidget=self.labelwidget, bd=5)
        self.label_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.frame = ttk.Frame(self.label_frame, padding=0)
        self.frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
                
        self.label = ttk.Label(
            self.frame,
            textvariable=self.joy_steer,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=15,
        )
        self.label.pack(ipadx=0, ipady=10)
        
        self.label = ttk.Label(
            self.frame,
            textvariable=self.joy_speed,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=15,
        )
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=0)
        self.frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        
        self.label = ttk.Label(
            self.frame,
            textvariable=self.joy_steer_percent,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=6,
        )
        self.label.pack(ipadx=0, ipady=10)
        
        self.label = ttk.Label(
            self.frame,
            textvariable=self.joy_speed_percent,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=6,
        )
        self.label.pack(ipadx=0, ipady=10)
        

        # Create a Frame for button read

        self.labelwidget = ttk.Label(self.main_frame, text="Button state",  font=("-size", self.size_title,"-weight", "bold"),)
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget, bd=5)
        self.label_frame.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
         
        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=0, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="Y",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="B",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=1, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label_Y = tk.Label(self.frame, image=self.btn_off)
        self.label_Y.pack(pady=15)
        self.label_B = tk.Label(self.frame, image=self.btn_off)
        self.label_B.pack(pady=15)

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=3, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="X",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="A",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=4, padx=(0, 0), pady=(20, 10), sticky="nsew")
        
        self.label_X = tk.Label(self.frame, image=self.btn_off)
        self.label_X.pack(pady=15)
        self.label_A = tk.Label(self.frame, image=self.btn_off)
        self.label_A.pack(pady=15)

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=5, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="L1",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="R1",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=6, padx=(0, 0), pady=(20, 10), sticky="nsew")
        
        self.label_L1 = tk.Label(self.frame, image=self.btn_off)
        self.label_L1.pack(pady=15)
        self.label_R1 = tk.Label(self.frame, image=self.btn_off)
        self.label_R1.pack(pady=15)
            
    def menu_start(self,init=1 ,increment=0):
        # Create menu_start
        self.page[0] = "menu"
        
        if init:
        
            self.clear()

            s = ttk.Style()
            s.configure('my.TButton', font=('Helvetica', 50))
            s = ttk.Style()
            s.configure('Accent.TButton', font=('Helvetica', 50))
            
            # Create a canvas
            self.canvas = tk.Canvas(self, width=800, height=500, bg="#e7e7e7")
            self.canvas.pack(fill="both", expand=True)

            # Set image in canvas
            self.canvas.create_image(0,0, image=self.bg_img, anchor="nw")
            
        self.position_menu=self.overflow(3,increment,self.position_menu)
            
        btn = []
        for i in range(4):
            btn.append('my.TButton')
            if self.position_menu == i:
                btn[i] = 'Accent.TButton'
        
        # Buttons
        self.button1 = ttk.Button(self, text="Mode pilotage",style=btn[0])
        self.button2 = ttk.Button(self, text="Information émetteur",style=btn[1])
        self.button3 = ttk.Button(self, text="Information récepteur",style=btn[2])        
        self.button4 = ttk.Button(self, text="Parametres",style=btn[3])   

        self.canvas.create_window(1280/2, 200, anchor="center", window=self.button1)
        self.canvas.create_window(1280/2, 300, anchor="center", window=self.button2)
        self.canvas.create_window(1280/2, 400, anchor="center", window=self.button3)
        self.canvas.create_window(1280/2, 500, anchor="center", window=self.button4)
        
    def print_param_joy(self,init=1 ,increment=0):

        self.page[1] = "joy"

        if Globale.inverse["direction_speed"]==True:speed_dir_inv =  self.switch_on
        else :speed_dir_inv=self.switch_off
        if Globale.inverse["direction_steer"]==True:steer_dir_inv =  self.switch_on
        else :steer_dir_inv=self.switch_off
        if Globale.inverse["steer_speed"]==True:speed_steer_inv =  self.switch_on
        else :speed_steer_inv=self.switch_off

        if init:
            self.clear()
            self.create_main_frame()

            # Create a Frame joystick param        
            self.labelwidget = ttk.Label(self.main_frame, text="Joystick inverse", font=("-size", self.size_title,"-weight", "bold"))
            self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
            self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew",ipadx=60,ipady=10)
                    
        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.position_param=self.overflow(3,increment,self.position_param)

        self.label = tk.Label(self.frame,text="Speed direction",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_param == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        self.label = tk.Label(self.frame,text="Steer direction",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_param == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        self.label = tk.Label(self.frame,text="Speed <-> steer ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_param == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
        self.label_speed_dir_inv = tk.Label(self.frame, image=speed_dir_inv)
        self.label_speed_dir_inv.pack(pady=15)
        self.label_steer_dir_inv = tk.Label(self.frame, image=steer_dir_inv)
        self.label_steer_dir_inv.pack(pady=15)
        self.label_speed_steer_inv = tk.Label(self.frame, image=speed_steer_inv)
        self.label_speed_steer_inv.pack(pady=15)

        if self.position_param == 3:
            btn = 'Accent.TButton'
        else:
            btn = 'my.TButton'
             
        self.button = ttk.Button(self.main_frame, text="Calibration joystick",style=btn)
        self.button.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
    
    def print_param_mode_normal(self,init=1 ,increment_y=0,increment_x=0):
        self.page[1] = "normal"

        if init:
            self.clear()
            self.create_main_frame()

        self.position_v=self.overflow(1,increment_y,self.position_v)
        self.position_h=self.overflow(1,increment_x,self.position_h)

        # Create a Frame        
        self.labelwidget = ttk.Label(self.main_frame, text="Coeff mode normal", font=("-size", self.size_title,"-weight", "bold"))
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew",ipadx=60,ipady=10)

        
        self.label = ttk.Label(self.label_frame,text="Speed = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=0, column=0, padx=(5), pady=(20, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.coef_speed_normal[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 0 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=1, padx=(5), pady=(20, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.coef_speed_normal[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 0 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=2, padx=(5), pady=(20, 10), sticky="nsew")          
        self.label = tk.Label(self.label_frame,text="%",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=0, column=3, padx=(0), pady=(20, 10), sticky="nsew")          
        
        self.label = ttk.Label(self.label_frame,text="Steer = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=1, column=0, padx=(5), pady=(20, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.coef_steer_normal[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 1 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=1, padx=(5), pady=(20, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.coef_steer_normal[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 1 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=2, padx=(5), pady=(20, 10), sticky="nsew")          
        self.label = tk.Label(self.label_frame,text="%",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=1, column=3, padx=(0), pady=(20, 10), sticky="nsew")    

    def print_param_mode_marteau(self,init=1 ,increment_y=0,increment_x=0):
        self.page[1] = "hammer"

        if init:
            self.clear()
            self.create_main_frame()


        self.position_v=self.overflow(4,increment_y,self.position_v)

        if self.position_v == 0 or self.position_v == 1:
            self.position_h=self.overflow(1,increment_x,self.position_h)
        else:
            self.position_h=self.overflow(3,increment_x,self.position_h)


        # Create a Frame        
        self.labelwidget = ttk.Label(self.main_frame, text="Coeff mode marteau", font=("-size", self.size_title,"-weight", "bold"))
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew",ipadx=60,ipady=0)
        
        self.label = ttk.Label(self.label_frame,text="Speed = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=0, column=0, padx=(5), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.coef_speed_hammer[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 0 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=1, padx=(5), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.coef_speed_hammer[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 0 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=2, padx=(5), pady=(10, 10), sticky="nsew")          
        self.label = tk.Label(self.label_frame,text="%",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=0, column=3, padx=(0), pady=(10, 10), sticky="nsew")          
        
        self.label = ttk.Label(self.label_frame,text="Steer = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=1, column=0, padx=(5), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.coef_steer_hammer[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 1 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=1, padx=(5), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.coef_steer_hammer[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 1 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=2, padx=(5), pady=(10, 10), sticky="nsew")          
        self.label = tk.Label(self.label_frame,text="%",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=1, column=3, padx=(0), pady=(10, 10), sticky="nsew")   

        # Create a Frame        
        self.labelwidget = ttk.Label(self.main_frame, text="PID", font=("-size", self.size_title,"-weight", "bold"))
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew",ipadx=60,ipady=10)

        
        self.label = ttk.Label(self.label_frame,text="P = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")           
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 3: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")          
        
        
        self.label = ttk.Label(self.label_frame,text="I = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")           
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 3: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        
        self.label = ttk.Label(self.label_frame,text="D = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")           
        self.label = tk.Label(self.label_frame,text="0",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 3: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")

    def parametres_widgets(self):
        
        self.page[0] = "parametres"
          
        self.create_main_frame()

        if self.page[1] == "hammer":
            self.print_param_mode_marteau()
        elif self.page[1] == "normal":
            self.print_param_mode_normal()
        else:
            self.print_param_joy()

    def recepteur_widgets(self):
        # Create recepteur_widgets
        self.page[0] = "receiver"
                   
        self.create_main_frame()
                
        self.current = ttk.Label(
            self.main_frame,
            textvariable=self.device_data,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.pack(ipadx=600, ipady=0)
        
        self.batterie = ttk.Label(
            self.main_frame,
            textvariable=self.joy_posY,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.batterie.pack(ipadx=600, ipady=0)
        
    def calibration_auto(self,mode):
        self.page[0] = "cal_auto"
        self.page[1] = mode
        
        self.clear()
        
        
        if mode=="no_move_x":
            instruction = "do not move X axis joystick"
        elif mode=="no_move_y":
            instruction = "do not move Y axis joystick"
        elif mode=="move_x":
            instruction = "move X axis joystick"
        elif mode=="move_y":
            instruction = "move Y axis joystick"
        else :
            instruction = "Erreur"
        
        
        self.create_main_frame()

        # Create calibration_auto_widgets
            
                
        self.current = ttk.Label(
            self.main_frame,
            text=instruction,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.pack(ipadx=0, ipady=0)
        
        self.current = ttk.Label(
            self.main_frame,
            textvariable=self.compteur_str,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.pack(ipadx=0, ipady=0)
        
    def calibration_result(self,joy_x_min,joy_x_middle,joy_x_max,joy_y_min,joy_y_middle,joy_y_max):  
        self.page = ["cal_auto","result"]

        self.clear()  
        self.create_main_frame()
        
        # Create a Frame calibration_result_widgets
                     
        self.labelwidget = ttk.Label(self.main_frame, text="Joystick X", font=("-size", self.size_title,"-weight", "bold"))
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
         
        self.current = ttk.Label(
            self.label_frame,
            text="max value = "+str(joy_x_max),
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=23,
        )
        self.current.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="middle value = "+str(joy_x_middle),
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="min value= "+str(joy_x_min),
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    
        # Create a Frame calibration_result_widgets
                     
        self.labelwidget = ttk.Label(self.main_frame, text="Joystick Y", font=("-size", self.size_title,"-weight", "bold"))
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")
         
        self.current = ttk.Label(
            self.label_frame,
            text="max value= "+str(joy_y_max),
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
            width=23,
        )
        self.current.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="middle value= "+str(joy_y_middle),
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="min value= "+str(joy_y_min),
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.current.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
      
    def manage_mode(self):
        if self.page[0] == "cal_auto":
                    if self.page[1] == "no_move_x":
                        Globale.joystick_x.calibration_middle_joystick(3,self.compteur_str.set)
                        if self.page[1] == "no_move_x":
                            self.calibration_auto("no_move_y")
                    elif self.page[1] == "no_move_y":
                        Globale.joystick_y.calibration_middle_joystick(3,self.compteur_str.set)
                        if self.page[1] == "no_move_y":
                            self.calibration_auto("move_x")
                    elif self.page[1] == "move_x":
                        Globale.joystick_x.calibration_max_min_joystick(7,self.compteur_str.set)
                        if self.page[1] == "move_x":
                            self.calibration_auto("move_y")
                    elif self.page[1] == "move_y":
                        Globale.joystick_y.calibration_max_min_joystick(7,self.compteur_str.set)
                        if self.page[1] == "move_y":
                            self.calibration_result(Globale.joystick_x.min_value,Globale.joystick_x.middle_value,Globale.joystick_x.max_value,Globale.joystick_y.min_value,Globale.joystick_y.middle_value,Globale.joystick_y.max_value)
                            save_param()

    def manage_up_down(self,direction):        
        if self.page[0] == "menu":
            self.menu_start(0,direction)       
        elif self.page[0] == "parametres":
            if self.page[1] == "joy":
                self.print_param_joy(0,direction)
            elif self.page[1] == "hammer":
                self.print_param_mode_marteau(0,direction,0)
            elif self.page[1] == "normal":
                self.print_param_mode_normal(0,direction,0)

    def manage_L1_R1(self,direction):      
        if self.page[0] == "parametres":

            if self.page[1] == "joy" and direction == 1:
                self.print_param_mode_marteau()
            elif self.page[1] == "joy" and direction == -1:
                self.print_param_mode_normal()    

            elif self.page[1] == "hammer" and direction == 1:
                self.print_param_mode_normal(1,0,0)
            elif self.page[1] == "hammer" and direction == -1:
                self.print_param_joy(1,0)

            elif self.page[1] == "normal" and direction == 1:
                self.print_param_joy(1,0)
            elif self.page[1] == "normal" and direction == -1:
                self.print_param_mode_marteau(1,0,0)

    def manage_left_right(self,direction):      
        if self.page[0] == "parametres":
            if self.page[1] == "hammer":
                self.print_param_mode_marteau(0,0,direction)
            elif self.page[1] == "normal":
                self.print_param_mode_normal(0,0,direction)