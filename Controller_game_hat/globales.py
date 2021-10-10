class Globale:
    
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
    
    joystick_current_value = {
    "X" : 512,
    "Y" : 512
    }
    
    joystick_current_value = {
    "X" : 512,
    "Y" : 512
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
        
    joystick_calibration = {
    "X" : 512,
    "Y" : 512
    }
    
    inverse = {
    "direction_speed" : 0,
    "direction_steer" : 0,
    "steer_speed" : 0
    }