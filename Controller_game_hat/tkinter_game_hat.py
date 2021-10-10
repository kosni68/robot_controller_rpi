import tkinter as tk
from tkinter import ttk
from globales import *
from bluetooth_rpi_thread import *

class App(ttk.Frame):
    
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        
        self.position_menu = 0

        # Create value lists
        self.page = ["controller","none"]
        #self.page_list = ["menu", "controller","receiver","parametres","cal_auto"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_5 = tk.DoubleVar(value=75.0)
        
        
        self.joy_real_x = tk.StringVar(value="X = ")
        self.joy_real_y = tk.StringVar(value="Y = ")
        self.joy_speed = tk.StringVar(value="Speed = ")
        self.joy_steer = tk.StringVar(value="Steer = ")
        self.device_data = tk.StringVar(value=str(Bluetooth_rpi.data))
        
        # Compteur variables
        self.compteur = 5
        self.compteur_str = tk.IntVar(value=str(self.compteur))
        

        # Create widgets :)
        self.emetteur_widgets()
        
    def clear(self):
            
        for widget in self.main_frame.winfo_children():
            widget.destroy()
   
    def select(self):
        if self.page[0] == "menu":
            self.clear()
            if self.position_menu ==0:
                self.emetteur_widgets()
            if self.position_menu ==1:
                self.recepteur_widgets()
            if self.position_menu ==2:
                self.parametres_widgets()
            if self.position_menu ==3:
                self.compteur_str.set(value=3)
                self.calibration_auto("no_move_x")
                
    def emetteur_widgets(self):
        # Create emetteur_widgets
        self.page[0] = "receiver"
            
        # Create a main Frame
                   
        self.main_frame = ttk.Frame(self, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
        # Create a Frame joystick read
        
        self.labelwidget = ttk.Label(self.main_frame, text="Joystick read", font=("-size", 32,"-weight", "bold"))
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
                
        self.label_joy_posX = ttk.Label(
            self.label_frame,
            textvariable=self.joy_real_x,
            justify="center",
            font=("-size", 30, "-weight", "bold"),
            width=23,
        )
        self.label_joy_posX.pack(ipadx=0, ipady=0)
        
        self.label_joy_posY = ttk.Label(
            self.label_frame,
            textvariable=self.joy_real_y,
            justify="left",
            font=("-size", 30, "-weight", "bold"),
            width=23,
        )
        self.label_joy_posY.pack(ipadx=0, ipady=0)
        
        # Create a Frame joystick send
        
        self.labelwidget = ttk.Label(self.main_frame, text="Joystick send",  font=("-size", 32,"-weight", "bold"),)
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget, bd=5)
        self.label_frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")
                
        self.label_joy_posX = ttk.Label(
            self.label_frame,
            textvariable=self.joy_steer,
            justify="center",
            font=("-size", 30, "-weight", "bold"),
            width=23,
        )
        self.label_joy_posX.pack(ipadx=0, ipady=0)
        
        self.label_joy_posY = ttk.Label(
            self.label_frame,
            textvariable=self.joy_speed,
            justify="center",
            font=("-size", 30, "-weight", "bold"),
        )
        self.label_joy_posY.pack(ipadx=0, ipady=0)
        
     
            
    def menu_start(self,init ,increment):
        # Create menu_start
        self.page[0] = "menu"
        
        self.clear()
        
        if init:
            
            self.columnconfigure(index=0, weight=1)
            self.rowconfigure(index=0, weight=1)
                
            # Create a Frame for input widgets
            self.main_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
            self.main_frame.grid(row=0, column=0, padx=100, pady=(300, 10), sticky="nsew", rowspan=4)
            
            self.main_frame.columnconfigure(index=0, weight=1)
        
            s = ttk.Style()
            s.configure('my.TButton', font=('Helvetica', 50))
            s = ttk.Style()
            s.configure('Accent.TButton', font=('Helvetica', 50))
            
        
        self.position_menu += increment
        if self.position_menu <0:
            self.position_menu = 3
        elif self.position_menu >3:
            self.position_menu = 0
            
        btn1 = 'my.TButton'
        btn2 = 'my.TButton'
        btn3 = 'my.TButton'
        btn4 = 'my.TButton'
        
        if self.position_menu == 0:
            btn1 = 'Accent.TButton'
        elif self.position_menu == 1:
            btn2 = 'Accent.TButton'
        elif self.position_menu == 2:
            btn3 = 'Accent.TButton'
        elif self.position_menu == 3:
            btn4 = 'Accent.TButton'
        
        # Buttons
        self.button1 = ttk.Button(self.main_frame, text="Information émetteur",style=btn1)
        self.button1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        
        self.button2 = ttk.Button(self.main_frame, text="Information récepteur",style=btn2)
        self.button2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        
        self.button3 = ttk.Button(self.main_frame, text="Parametres",style=btn3)
        self.button3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        
        self.button4 = ttk.Button(self.main_frame, text="Calibration joystick",style=btn4)
        self.button4.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        
    def parametres_widgets(self):
        # Create parametres_widgets
        
        self.page[0] = "parametres"
          
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
            
        # Create a main Frame
                   
        self.main_frame = ttk.Frame(self, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
        # Create a Frame
        
        self.labelwidget = ttk.Label(self.main_frame, text="test", font=("-size", 25),)
        
        self.label_frame = ttk.LabelFrame(self.main_frame, labelwidget=self.labelwidget, padding=(20, 10))
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
        s = ttk.Style()
        s.configure('Switch.TCheckbutton', font=('Helvetica', 25))
        
        # Switch
        self.switch = ttk.Checkbutton(self.label_frame, text="Inversion joystick X", style="Switch.TCheckbutton", variable=self.var_0)
        self.switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        
        self.switch = ttk.Checkbutton(self.label_frame, text="Inversion joystick Y", style="Switch.TCheckbutton", variable=self.var_1)
        self.switch.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        
        self.switch = ttk.Checkbutton(self.label_frame, text="Enable correction", style="Switch.TCheckbutton", variable=self.var_2)
        self.switch.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        
        # Create a Frame
        self.radio_frame = ttk.LabelFrame(self.main_frame, text="Radiobuttons", padding=(20, 10))
        self.radio_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        
        self.label = ttk.Label(self.radio_frame, text="vitesse", font=("-size", 25),)
        self.label.grid(row=0, column=0, pady=10, columnspan=2,sticky="nsew")
        
        # Scale
        self.scale = ttk.Scale(self.radio_frame,from_=100,to=0,variable=self.var_5,command=lambda event: self.var_5.set(self.scale.get()),)
        self.scale.grid(row=0, column=1, padx=(0, 10), pady=(20, 0), sticky="ew")

        # Progressbar
        self.progress = ttk.Progressbar(self.radio_frame, value=0, variable=self.var_5, mode="determinate")
        self.progress.grid(row=0, column=2, padx=(10, 20), pady=(20, 0), sticky="ew")
      
    def recepteur_widgets(self):
        # Create recepteur_widgets
        self.page[0] = "receiver"
                   
        self.main_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.main_frame.grid(row=0, column=0, padx=100, pady=(100, 10), sticky="nsew", rowspan=3)
                
        self.current = ttk.Label(
            self.main_frame,
            textvariable=self.device_data,
            justify="center",
            font=("-size", 30, "-weight", "bold"),
        )
        self.current.pack(ipadx=600, ipady=0)
        
        self.batterie = ttk.Label(
            self.main_frame,
            textvariable=self.joy_posY,
            justify="center",
            font=("-size", 30, "-weight", "bold"),
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
        
        
        # Create calibration_auto_widgets
            
        self.main_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.main_frame.grid(row=0, column=0, padx=100, pady=(300, 10), sticky="nsew", rowspan=4)
                
        self.current = ttk.Label(
            self.main_frame,
            text=instruction,
            justify="center",
            font=("-size", 40, "-weight", "bold"),
        )
        self.current.pack(ipadx=0, ipady=0)
        
        self.current = ttk.Label(
            self.main_frame,
            textvariable=self.compteur_str,
            justify="center",
            font=("-size", 50, "-weight", "bold"),
        )
        self.current.pack(ipadx=0, ipady=0)
        
    
    def calibration_result(self,joy_x_min,joy_x_middle,joy_x_max,joy_y_min,joy_y_middle,joy_y_max):  
        self.page = ["cal_auto","result"]
            
        # Create a main Frame
                   
        self.main_frame = ttk.Frame(self, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
        # Create a Frame calibration_result_widgets
                     
        self.labelwidget = ttk.Label(self.main_frame, text="Joystick X", font=("-size", 32,"-weight", "bold"))
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
         
        self.current = ttk.Label(
            self.label_frame,
            text="max value = "+str(joy_x_max),
            justify="center",
            font=("-size", 40, "-weight", "bold"),
            width=23,
        )
        self.current.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="middle value = "+str(joy_x_middle),
            justify="center",
            font=("-size", 40, "-weight", "bold"),
        )
        self.current.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="min value= "+str(joy_x_min),
            justify="center",
            font=("-size", 40, "-weight", "bold"),
        )
        self.current.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    
        # Create a Frame calibration_result_widgets
                     
        self.labelwidget = ttk.Label(self.main_frame, text="Joystick Y", font=("-size", 32,"-weight", "bold"))
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")
         
        self.current = ttk.Label(
            self.label_frame,
            text="max value= "+str(joy_y_max),
            justify="center",
            font=("-size", 40, "-weight", "bold"),
            width=23,
        )
        self.current.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="middle value= "+str(joy_y_middle),
            justify="center",
            font=("-size", 40, "-weight", "bold"),
        )
        self.current.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        
        self.current = ttk.Label(
            self.label_frame,
            text="min value= "+str(joy_y_min),
            justify="center",
            font=("-size", 40, "-weight", "bold"),
        )
        self.current.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
      
