from globales import *
import json

def save_param():
    struct_config = {"joystick_x": {"max_value": Globale.joystick_x.max_value,
                                    "middle_value": Globale.joystick_x.middle_value,
                                    "min_value": Globale.joystick_x.min_value
                                    },
                     "joystick_y": {"max_value": Globale.joystick_x.max_value,
                                    "middle_value": Globale.joystick_x.middle_value,
                                    "min_value": Globale.joystick_x.min_value
                                    },
                     "param": {"inverse": Globale.inverse
                            },
                }

    with open('controller_config.json', 'w') as file:
        json.dump(struct_config, file)

def load_param():
    with open('controller_config.json', 'r') as file:
        datadict = json.load(file)
        
    Globale.joystick_x.max_value=datadict["joystick_x"]["max_value"]
    Globale.joystick_x.middle_value=datadict["joystick_x"]["middle_value"]
    Globale.joystick_x.min_value=datadict["joystick_x"]["min_value"]
    
    Globale.joystick_y.max_value=datadict["joystick_y"]["max_value"]
    Globale.joystick_y.middle_value=datadict["joystick_y"]["middle_value"]
    Globale.joystick_y.min_value=datadict["joystick_y"]["min_value"]
    
    Globale.inverse=datadict["param"]["inverse"]