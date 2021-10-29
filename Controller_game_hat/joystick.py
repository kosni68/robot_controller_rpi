from ADS1115 import *
import time

class Joystick():
    
    def __init__(self,address,port_ads,resolution,dead_zone):
        self.ads1115 = ADS1115(address)
        self.current_read_value = 0
        self.max_value = resolution
        self.min_value = 0
        self.middle_value = resolution/2
        self.dead_zone = dead_zone
        self.resolution = resolution
        self.port_ads = port_ads
        
    def _map(self,x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def read_joystick(self):
        self.current_read_value=self.ads1115.analog_read(self.port_ads)
            
    def calibration_middle_joystick(self,tempo_time,time_print):
        
        middle_value_moyenne=self.ads1115.analog_read(self.port_ads)
        iterrator=1
        
        start_time=time.time()
        while time.time() - start_time < tempo_time :
            time_print(value=round(tempo_time-(time.time() - start_time)))
            middle_value_moyenne+=self.ads1115.analog_read(self.port_ads)
            iterrator+=1
            
        self.middle_value = round(middle_value_moyenne/iterrator)
        
    def calibration_max_min_joystick(self,tempo_time,time_print):
        
        max_value=self.ads1115.analog_read(self.port_ads)
        min_value=self.ads1115.analog_read(self.port_ads)
        
        start_time=time.time()
        while time.time() - start_time < tempo_time:
            time_print(value=round(tempo_time-(time.time() - start_time)))
            self.current_read_value=self.ads1115.analog_read(self.port_ads)
            
            if self.current_read_value < min_value:
                min_value=self.current_read_value
                
            if self.current_read_value > max_value:
                max_value=self.current_read_value                
                
        self.max_value = max_value
        self.min_value = min_value

    def scale_current_value(self,inverse_dir):
        
        self.current_read_value=self.ads1115.analog_read(self.port_ads)
        
        if self.current_read_value > self.middle_value - self.dead_zone and self.current_read_value < self.middle_value + self.dead_zone :
            return round(self.resolution/2)
        
        elif self.current_read_value > self.middle_value + self.dead_zone:
            return_value = self._map(self.current_read_value, self.middle_value + self.dead_zone,self.max_value,self.resolution/2,self.resolution)
            if (return_value > self.resolution):
                return_value = self.resolution
            
        elif self.current_read_value < self.middle_value - self.dead_zone:
            return_value = self._map(self.current_read_value, self.middle_value - self.dead_zone,self.min_value,self.resolution/2,0)
            if (return_value < 0):
                return_value = 0
                
        if inverse_dir:
            return_value=self.resolution-return_value
            
        return return_value
            
