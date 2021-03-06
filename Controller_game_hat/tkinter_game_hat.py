import tkinter as tk
from tkinter import ttk
from globales import *
from udp_client import *
from Config.config import *

class Tkinter_app(ttk.Frame):
    
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.bg_img = tk.PhotoImage(file="img/background2.png")
        self.btn_on = tk.PhotoImage(file="img/btn_on.png")
        self.btn_off = tk.PhotoImage(file="img/btn_off.png")
        self.switch_on = tk.PhotoImage(file="img/switch-on.png")
        self.switch_off = tk.PhotoImage(file="img/switch-off.png")

        self.battery_100 = tk.PhotoImage(file="img/battery_100.png")
        self.battery_80 = tk.PhotoImage(file="img/battery_80.png")
        self.battery_60 = tk.PhotoImage(file="img/battery_60.png")
        self.battery_40 = tk.PhotoImage(file="img/battery_40.png")
        self.battery_20 = tk.PhotoImage(file="img/battery_20.png")
        self.battery_0 = tk.PhotoImage(file="img/battery_0.png")

        self.position_menu = 0
        self.position_param =0
        self.position_v = 0
        self.position_h = 0
        self.size_title=50
        self.size_item=40
        self.fg_title="#56C7FC"
        self.bg_color ="#1c1c1c"
        # Create value lists
        self.page = ["",""]
        #self.page_list = ["menu", "controller","robot","parametres","cal_auto"]

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

        self.pid_p = [tk.StringVar(value="0"),tk.StringVar(value="0"),tk.StringVar(value="0"),tk.StringVar(value="0")]
        self.pid_i = [tk.StringVar(value="0"),tk.StringVar(value="0"),tk.StringVar(value="0"),tk.StringVar(value="0")]
        self.pid_d = [tk.StringVar(value="0"),tk.StringVar(value="0"),tk.StringVar(value="0"),tk.StringVar(value="0")]

        self.mode_hammer_robot = tk.StringVar(value="")

        self.joy_real_x = tk.StringVar(value="X = ")
        self.joy_real_y = tk.StringVar(value="Y = ")
        self.joy_speed = tk.StringVar(value="Speed = ")
        self.joy_steer = tk.StringVar(value="Steer = ")
        self.joy_speed_percent = tk.StringVar(value="")
        self.joy_steer_percent = tk.StringVar(value="")

        self.feedback_cmd1 = tk.IntVar(value=0)
        self.feedback_cmd2 = tk.IntVar(value=0)
        self.feedback_speedR_meas = tk.IntVar(value=0)
        self.feedback_speedL_meas = tk.IntVar(value=0)
        self.feedback_batVoltage = tk.IntVar(value=0)
        self.feedback_boardTemp = tk.IntVar(value=0)
        self.feedback_Temperature = tk.IntVar(value=0)
        self.feedback_cmdLed = tk.IntVar(value=0)
        self.imu_roll = tk.IntVar(value=0)
        self.imu_pitch = tk.IntVar(value=0)
        
        # Compteur variables
        self.compteur = 5
        self.compteur_str = tk.IntVar(value=str(self.compteur))

        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 50))
        s.configure('Accent.TButton', font=('Helvetica', 50))
        
        self.print_menu_start()
     
    def overflow(self,limite,increment,value):
        value += increment
        if value <0:
            value = limite
        elif value >limite:
            value = 0
        
        return value

    def update(self):

        if self.page[0] == "pilotage":
            if not Globale.mode_hammer_robot:
                self.mode_hammer_robot.set(value="L1< NORMAL >R1")
                self.label_mode_robot.config(fg="#3bfd00")
            elif Globale.mode_hammer_robot:
                self.mode_hammer_robot.set(value="L1< HAMMER >R1")
                self.label_mode_robot.config(fg="#007cff")
            else:
                self.mode_hammer_robot.set(value="L1< ERREUR >R1")
                self.label_mode_robot.config(fg="#ff0000")

        elif self.page[0] == "controller":
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
            
        elif self.page[0] == "robot":

            self.feedback_cmd1.set(value=Globale.hoverboard_feed_back["cmd1"])
            self.feedback_cmd2.set(value=Globale.hoverboard_feed_back["cmd2"])
            self.feedback_speedR_meas.set(value=Globale.hoverboard_feed_back["speedR_meas"])
            self.feedback_speedL_meas.set(value=Globale.hoverboard_feed_back["speedL_meas"])
            self.feedback_batVoltage.set(value=Globale.hoverboard_feed_back["batVoltage"])
            self.feedback_boardTemp.set(value=Globale.hoverboard_feed_back["boardTemp"])
            self.feedback_Temperature.set(value=Globale.hoverboard_feed_back["Temperature"])
            self.feedback_cmdLed.set(value=Globale.hoverboard_feed_back["cmdLed"])

            self.imu_roll.set(value=Globale.hoverboard_feed_back["Roll"])
            self.imu_pitch.set(value=Globale.hoverboard_feed_back["Pitch"])
    
        elif self.page[0] == "parametres":

            if self.page[1] == "normal":
                self.coef_speed_normal[0].set(value=str(Globale.coef_normal["speed_10"]))
                self.coef_speed_normal[1].set(value=str(Globale.coef_normal["speed_1"]))

                self.coef_steer_normal[0].set(value=str(Globale.coef_normal["steer_10"]))
                self.coef_steer_normal[1].set(value=str(Globale.coef_normal["steer_1"]))

            elif self.page[1] == "hammer":
                self.coef_speed_hammer[0].set(value=str(Globale.coef_hammer["speed_10"]))
                self.coef_speed_hammer[1].set(value=str(Globale.coef_hammer["speed_1"]))

                self.coef_steer_hammer[0].set(value=str(Globale.coef_hammer["steer_10"]))
                self.coef_steer_hammer[1].set(value=str(Globale.coef_hammer["steer_1"]))

                self.pid_p[0].set(value=str(Globale.P["1000"]))
                self.pid_p[1].set(value=str(Globale.P["100"]))
                self.pid_p[2].set(value=str(Globale.P["10"]))
                self.pid_p[3].set(value=str(Globale.P["1"]))

                self.pid_i[0].set(value=str(Globale.I["1000"]))
                self.pid_i[1].set(value=str(Globale.I["100"]))
                self.pid_i[2].set(value=str(Globale.I["10"]))
                self.pid_i[3].set(value=str(Globale.I["1"]))

                self.pid_d[0].set(value=str(Globale.D["1000"]))
                self.pid_d[1].set(value=str(Globale.D["100"]))
                self.pid_d[2].set(value=str(Globale.D["10"]))
                self.pid_d[3].set(value=str(Globale.D["1"]))

    def create_main_frame(self):

        self.main_frame = ttk.Frame(self, padding=(10, 10))
        self.main_frame.pack(pady=10)
            
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
                Globale.acces_send_data=1
                self.print_info_pilotage()
            elif self.position_menu ==1:
                Globale.acces_send_data=1
                self.print_info_controller()
            elif self.position_menu ==2:
                Globale.acces_send_data=1
                self.print_info_robot()
            elif self.position_menu ==3:
                Globale.acces_send_data=0
                self.print_param()

        elif self.page[0] == "parametres":
            if self.page[1] == "joy":
                if self.position_param ==0:
                    Globale.inverse["direction_speed"]= not Globale.inverse["direction_speed"]
                    if Globale.inverse["direction_speed"]==True:self.label_speed_dir_inv.configure(image=self.switch_on) 
                    else :self.label_speed_dir_inv.configure(image=self.switch_off)
                    save_param()
                elif self.position_param ==1:
                    Globale.inverse["direction_steer"]= not Globale.inverse["direction_steer"]
                    if Globale.inverse["direction_steer"]==True:self.label_steer_dir_inv.configure(image=self.switch_on) 
                    else :self.label_steer_dir_inv.configure(image=self.switch_off)
                    save_param()
                elif self.position_param ==2:
                    Globale.inverse["steer_speed"]= not Globale.inverse["steer_speed"]
                    if Globale.inverse["steer_speed"]==True:self.label_speed_steer_inv.configure(image=self.switch_on) 
                    else :self.label_speed_steer_inv.configure(image=self.switch_off)
                    save_param()
                elif self.position_param ==3:
                    self.compteur_str.set(value=3)
                    self.calibration_auto("no_move_x")
            
            elif self.page[1] == "normal":
                if self.position_v == 0 and self.position_h == 0 : 
                    Globale.coef_normal["speed_10"]+=1
                    Globale.coef_normal["speed_10"]=self.overflow(9,0,Globale.coef_normal["speed_10"])
                elif self.position_v == 0 and self.position_h == 1 : 
                    Globale.coef_normal["speed_1"]+=1
                    Globale.coef_normal["speed_1"]=self.overflow(9,0,Globale.coef_normal["speed_1"])
                elif self.position_v == 1 and self.position_h == 0 : 
                    Globale.coef_normal["steer_10"]+=1
                    Globale.coef_normal["steer_10"]=self.overflow(9,0,Globale.coef_normal["steer_10"])
                elif self.position_v == 1 and self.position_h == 1 : 
                    Globale.coef_normal["steer_1"]+=1
                    Globale.coef_normal["steer_1"]=self.overflow(9,0,Globale.coef_normal["steer_1"])
            
            elif self.page[1] == "hammer":
                if self.position_v == 0 and self.position_h == 0 : 
                    Globale.coef_hammer["speed_10"]+=1
                    Globale.coef_hammer["speed_10"]=self.overflow(9,0,Globale.coef_hammer["speed_10"])
                elif self.position_v == 0 and self.position_h == 1 : 
                    Globale.coef_hammer["speed_1"]+=1
                    Globale.coef_hammer["speed_1"]=self.overflow(9,0,Globale.coef_hammer["speed_1"])
                elif self.position_v == 1 and self.position_h == 0 : 
                    Globale.coef_hammer["steer_10"]+=1
                    Globale.coef_hammer["steer_10"]=self.overflow(9,0,Globale.coef_hammer["steer_10"])
                elif self.position_v == 1 and self.position_h == 1 : 
                    Globale.coef_hammer["steer_1"]+=1
                    Globale.coef_hammer["steer_1"]=self.overflow(9,0,Globale.coef_hammer["steer_1"])

                elif self.position_v == 2:
                    liste_pid=["1000","100","10","1"]
                    for i in range(len(liste_pid)):
                        if self.position_h == i: 
                            Globale.P[liste_pid[i]]+=1
                            Globale.P[liste_pid[i]]=self.overflow(9,0,Globale.P[liste_pid[i]])

                elif self.position_v == 3:
                    liste_pid=["1000","100","10","1"]
                    for i in range(len(liste_pid)):
                        if self.position_h == i: 
                            Globale.I[liste_pid[i]]+=1
                            Globale.I[liste_pid[i]]=self.overflow(9,0,Globale.I[liste_pid[i]])

                elif self.position_v == 4:
                    liste_pid=["1000","100","10","1"]
                    for i in range(len(liste_pid)):
                        if self.position_h == i: 
                            Globale.D[liste_pid[i]]+=1
                            Globale.D[liste_pid[i]]=self.overflow(9,0,Globale.D[liste_pid[i]])
            
                save_param()
              
    def print_info_pilotage(self):
        self.page[0] = "pilotage"

        self.create_main_frame()

        self.labelwidget = tk.Label(self.main_frame, text="Mode", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
                
        self.label_mode_robot = tk.Label(
            self.label_frame,
            textvariable=self.mode_hammer_robot,
            justify="center",
            font=("-size", self.size_item, "-weight", "bold"),
        )
        self.label_mode_robot.pack(ipadx=0, ipady=0)

        # Create a Frame mode

        self.mode_frame = tk.Frame(self.main_frame)
        self.mode_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        # Create a Frame battery
        
        self.labelwidget = tk.Label(self.mode_frame, text="Battery",  font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
        self.label_frame = tk.LabelFrame(self.mode_frame, labelwidget=self.labelwidget, bd=5)
        self.label_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="Robot",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=8,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="Controller",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=8,)
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=1, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="4.5V",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="2.1V",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=2, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label_controller_bat = tk.Label(self.frame, image=self.battery_100)
        self.label_controller_bat.pack(pady=10)
        self.label_robot_bat = tk.Label(self.frame, image=self.battery_20)
        self.label_robot_bat.pack(pady=10)

        # Create a Frame Current

        self.labelwidget = tk.Label(self.mode_frame, text="Current", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)

        self.label_frame = tk.LabelFrame(self.mode_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
                
        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="right wheel",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=10,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="left wheel",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=10,)
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=1, padx=(0, 0), pady=(20, 10), sticky="nsew")

        self.label = ttk.Label(self.frame,text="0.5A",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="0.7A",justify="center",font=("-size", self.size_item, "-weight", "bold"))
        self.label.pack(ipadx=0, ipady=10)

        self.update()

    def print_info_controller(self):
        self.page[0] = "controller"

        self.create_main_frame()

        self.joy_frame = tk.Frame(self.main_frame)
        self.joy_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Create a Frame joystick read
        
        self.labelwidget = tk.Label(self.joy_frame, text="Joy read", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
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
        
        self.labelwidget = tk.Label(self.joy_frame, text="Joy send",  font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
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

        self.labelwidget = tk.Label(self.main_frame, text="Button state",  font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
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
            
    def print_menu_start(self):
        self.page[0] = "menu"
        
        self.clear()
            
        # Create a canvas
        self.canvas = tk.Canvas(self, width=800, height=500, bg="#e7e7e7")
        self.canvas.pack(fill="both", expand=True)

        # Set image in canvas
        self.canvas.create_image(0,0, image=self.bg_img, anchor="nw")
            
        self.button=[]
        # Buttons
        self.button.append(ttk.Button(self, text="Mode pilotage",style='my.TButton'))
        self.button.append(ttk.Button(self, text="Info controller",style='my.TButton'))
        self.button.append(ttk.Button(self, text="Info robot",style='my.TButton'))       
        self.button.append(ttk.Button(self, text="Parametres",style='my.TButton'))  

        for i in range(len(self.button)):
            if self.position_menu == i:
                self.button[i].configure(style='Accent.TButton')

        self.canvas.create_window(1280/2, 200, anchor="center", window=self.button[0])
        self.canvas.create_window(1280/2, 300, anchor="center", window=self.button[1])
        self.canvas.create_window(1280/2, 400, anchor="center", window=self.button[2])
        self.canvas.create_window(1280/2, 500, anchor="center", window=self.button[3])
        
    def print_param_joy(self):

        self.page[1] = "joy"

        if Globale.inverse["direction_speed"]==True:speed_dir_inv =  self.switch_on
        else :speed_dir_inv=self.switch_off
        if Globale.inverse["direction_steer"]==True:steer_dir_inv =  self.switch_on
        else :steer_dir_inv=self.switch_off
        if Globale.inverse["steer_speed"]==True:speed_steer_inv =  self.switch_on
        else :speed_steer_inv=self.switch_off

        self.clear()
        self.create_main_frame()

        # Create a Frame joystick param        
        self.labelwidget = tk.Label(self.main_frame, text="Joystick inverse", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew",ipadx=60,ipady=10)
                    
        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.label_switch_param_joy=[]

        self.label_switch_param_joy.append(tk.Label(self.frame,text="Speed direction",justify="left",font=("-size", self.size_item, "-weight", "bold")))
        self.label_switch_param_joy[0].grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.label_switch_param_joy.append(tk.Label(self.frame,text="Steer direction",justify="left",font=("-size", self.size_item, "-weight", "bold")))
        self.label_switch_param_joy[1].grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.label_switch_param_joy.append(tk.Label(self.frame,text="Speed <-> steer ",justify="left",font=("-size", self.size_item, "-weight", "bold")))
        self.label_switch_param_joy[2].grid(row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        for i in range(len(self.label_switch_param_joy)):
            if self.position_param == i: 
                self.label_switch_param_joy[i].config(bg= "#56C7FC", fg= "black")

        self.frame = ttk.Frame(self.label_frame, padding=(20, 10))
        self.frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
        self.label_speed_dir_inv = tk.Label(self.frame, image=speed_dir_inv)
        self.label_speed_dir_inv.pack(pady=15)
        self.label_steer_dir_inv = tk.Label(self.frame, image=steer_dir_inv)
        self.label_steer_dir_inv.pack(pady=15)
        self.label_speed_steer_inv = tk.Label(self.frame, image=speed_steer_inv)
        self.label_speed_steer_inv.pack(pady=15)
             
        self.button_calib_joy = ttk.Button(self.main_frame, text="Calibration joystick",style='my.TButton')
        self.button_calib_joy.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        if self.position_param == 3:
            self.button_calib_joy.configure(style='Accent.TButton')
    
    def print_param_mode_normal(self,init=1 ,increment_y=0,increment_x=0):
        self.page[1] = "normal"

        if init:
            self.clear()
            self.create_main_frame()
            self.update()

        self.position_v=self.overflow(1,increment_y,self.position_v)
        self.position_h=self.overflow(1,increment_x,self.position_h)

        # Create a Frame        
        self.labelwidget = tk.Label(self.main_frame, text="Coeff mode normal", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
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
            self.update()

        self.position_v=self.overflow(4,increment_y,self.position_v)

        if self.position_v == 0 or self.position_v == 1:
            self.position_h=self.overflow(1,increment_x,self.position_h)
        else:
            self.position_h=self.overflow(3,increment_x,self.position_h)


        # Create a Frame        
        self.labelwidget = tk.Label(self.main_frame, text="Coeff mode marteau", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
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
        self.labelwidget = tk.Label(self.main_frame, text="PID", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew",ipadx=60,ipady=10)

        
        self.label = ttk.Label(self.label_frame,text="P = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.pid_p[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.pid_p[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.pid_p[2],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")           
        self.label = tk.Label(self.label_frame,textvariable=self.pid_p[3],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 2 and self.position_h == 3: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=0, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")          
        
        
        self.label = ttk.Label(self.label_frame,text="I = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.pid_i[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.label = tk.Label(self.label_frame,textvariable=self.pid_i[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.pid_i[2],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")           
        self.label = tk.Label(self.label_frame,textvariable=self.pid_i[3],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 3 and self.position_h == 3: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=1, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
        

        self.label = ttk.Label(self.label_frame,text="D = ",justify="left",font=("-size", self.size_item, "-weight", "bold"))
        self.label.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")    
        self.label = tk.Label(self.label_frame,textvariable=self.pid_d[0],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 0: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.label = tk.Label(self.label_frame,textvariable=self.pid_d[1],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 1: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
        self.label = tk.Label(self.label_frame,textvariable=self.pid_d[2],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 2: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")           
        self.label = tk.Label(self.label_frame,textvariable=self.pid_d[3],justify="left",font=("-size", self.size_item, "-weight", "bold"))
        if self.position_v == 4 and self.position_h == 3: self.label.config(bg= "#56C7FC", fg= "black")
        self.label.grid(row=2, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")

    def print_param(self):
        
        self.page[0] = "parametres"
          
        self.create_main_frame()

        if self.page[1] == "hammer":
            self.print_param_mode_marteau()
        elif self.page[1] == "normal":
            self.print_param_mode_normal()
        else:
            self.print_param_joy()

    def print_info_robot(self):
        self.page[0] = "robot"
                   
        self.create_main_frame()
                
        # Create a Frame Feedback

        self.labelwidget = tk.Label(self.main_frame, text="Feedback", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)

        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
                
        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,text="Cmd1: ",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="Cmd2:",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)
        self.label = ttk.Label(self.frame,text="speedR: ",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="speedL:",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)    
        
        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,text="batVoltage: ",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=10,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,text="boardTemp:",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=10,)
        self.label.pack(ipadx=0, ipady=10)       
        self.label = ttk.Label(self.frame,text="Temp:",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=10,)
        self.label.pack(ipadx=0, ipady=10)       
        self.label = ttk.Label(self.frame,text="cmdLed:",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=10,)
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,textvariable=self.feedback_cmd1,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,textvariable=self.feedback_cmd2,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)
        self.label = ttk.Label(self.frame,textvariable=self.feedback_speedR_meas,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,textvariable=self.feedback_speedL_meas,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=4, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,textvariable=self.feedback_batVoltage,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,textvariable=self.feedback_boardTemp,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)
        self.label = ttk.Label(self.frame,textvariable=self.feedback_Temperature,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)        
        self.label = ttk.Label(self.frame,textvariable=self.feedback_cmdLed,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)
        
        # Create a Frame IMU

        self.labelwidget = tk.Label(self.main_frame, text="IMU", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)

        self.label_frame = tk.LabelFrame(self.main_frame, labelwidget=self.labelwidget,bd=5)
        self.label_frame.grid(row=1, column=0, padx=(0, 10), pady=(10, 10), sticky="nsew")
                
        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,text="Roll: ",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)  

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,textvariable=self.imu_roll,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)   

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,text="Pitch: ",justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)   

        self.frame = ttk.Frame(self.label_frame, padding=(10, 10))
        self.frame.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label = ttk.Label(self.frame,textvariable=self.imu_pitch,justify="center",font=("-size", self.size_item, "-weight", "bold"),width=7,)
        self.label.pack(ipadx=0, ipady=10)   

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
        
    def print_calibration_result(self,joy_x_min,joy_x_middle,joy_x_max,joy_y_min,joy_y_middle,joy_y_max):  
        self.page = ["cal_auto","result"]

        self.clear()  
        self.create_main_frame()
        
        # Create a Frame calibration_result_widgets
                     
        self.labelwidget = tk.Label(self.main_frame, text="Joystick X", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
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
                     
        self.labelwidget = tk.Label(self.main_frame, text="Joystick Y", font=("-size", self.size_title,"-weight", "bold"),fg=self.fg_title)
        
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
                            self.print_calibration_result(Globale.joystick_x.min_value,Globale.joystick_x.middle_value,Globale.joystick_x.max_value,Globale.joystick_y.min_value,Globale.joystick_y.middle_value,Globale.joystick_y.max_value)
                            save_param()

    def manage_up_down(self,direction):
        if self.page[0] == "menu":

            self.position_menu=self.overflow(3,direction,self.position_menu)
            for i in range(len(self.button)):
                if self.position_menu == i:
                    self.button[i].configure(style='Accent.TButton')
                else:
                    self.button[i].configure(style='my.TButton')
                    
        elif self.page[0] == "parametres":
            if self.page[1] == "joy":
                self.position_param=self.overflow(3,direction,self.position_param)
                for i in range(len(self.label_switch_param_joy)):
                    self.label_switch_param_joy[i].config(bg= self.bg_color, fg= "white")
                    self.button_calib_joy.configure(style='my.TButton')
                    if self.position_param == i: 
                        self.label_switch_param_joy[i].config(bg= "#56C7FC", fg= "black")
                    elif self.position_param == 3:
                        self.button_calib_joy.configure(style='Accent.TButton')

            elif self.page[1] == "hammer":
                self.print_param_mode_marteau(0,direction,0)
            elif self.page[1] == "normal":
                self.print_param_mode_normal(0,direction,0)

    def manage_L1_R1(self,direction):

        if self.page[0] == "pilotage":
            Globale.mode_hammer_robot = self.overflow(1,direction,Globale.mode_hammer_robot)

        elif self.page[0] == "parametres":

            if self.page[1] == "joy" and direction == 1:
                self.print_param_mode_marteau()
            elif self.page[1] == "joy" and direction == -1:
                self.print_param_mode_normal()    

            elif self.page[1] == "hammer" and direction == 1:
                self.print_param_mode_normal(1,0,0)
            elif self.page[1] == "hammer" and direction == -1:
                self.print_param_joy()

            elif self.page[1] == "normal" and direction == 1:
                self.print_param_joy()
            elif self.page[1] == "normal" and direction == -1:
                self.print_param_mode_marteau(1,0,0)

    def manage_left_right(self,direction):
        if self.page[0] == "parametres":
            if self.page[1] == "hammer":
                self.print_param_mode_marteau(0,0,direction)
            elif self.page[1] == "normal":
                self.print_param_mode_normal(0,0,direction)