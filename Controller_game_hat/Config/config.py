from globales import *
import json

def save_param():

    pid = {
    "P" : Globale.P,
    "I" : Globale.I,
    "D" : Globale.D
    }

    struct_config = {"joystick_x": {"max_value": Globale.joystick_x.max_value,
                                    "middle_value": Globale.joystick_x.middle_value,
                                    "min_value": Globale.joystick_x.min_value
                                    },
                     "joystick_y": {"max_value": Globale.joystick_x.max_value,
                                    "middle_value": Globale.joystick_x.middle_value,
                                    "min_value": Globale.joystick_x.min_value
                                    },
                     "param": {"inverse": Globale.inverse,
                               "coef_normal": Globale.coef_normal,
                               "coef_hammer": Globale.coef_hammer,
                               "pid": pid,
                            },
                }

    with open('Config/controller_config.json', 'w') as file:
        json.dump(struct_config, file)

def load_param():
    with open('Config/controller_config.json', 'r') as file:
        datadict = json.load(file)
        
    Globale.joystick_x.max_value=datadict["joystick_x"]["max_value"]
    Globale.joystick_x.middle_value=datadict["joystick_x"]["middle_value"]
    Globale.joystick_x.min_value=datadict["joystick_x"]["min_value"]
    
    Globale.joystick_y.max_value=datadict["joystick_y"]["max_value"]
    Globale.joystick_y.middle_value=datadict["joystick_y"]["middle_value"]
    Globale.joystick_y.min_value=datadict["joystick_y"]["min_value"]
    
    Globale.inverse=datadict["param"]["inverse"]
    Globale.coef_normal=datadict["param"]["coef_normal"]
    Globale.coef_hammer=datadict["param"]["coef_hammer"]
    
    pid=datadict["param"]["pid"]
    Globale.P=pid["P"]
    Globale.I=pid["I"]
    Globale.D=pid["D"]
