# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# sudo python3 -m pip install pybluez
# 
# sudo bluetoothctl
# power on
# agent NoInputNoOutput
# default-agent
# discoverable on
# scan on
# trust B8:27:EB:A1:C0:9B
# connect B8:27:EB:A1:C0:9B

import bluetooth
import threading
import time
from globales import Globale

class Bluetooth_rpi:
    server_sock = None
    client_sock = None
    sock = None
    data = None
    port = 1
    targetBluetoothMacAddress="B8:27:EB:A1:C0:9B"
    
    def connection():
        Bluetooth_rpi.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        Bluetooth_rpi.sock.connect((Bluetooth_rpi.targetBluetoothMacAddress, Bluetooth_rpi.port))
        print ("connected")

    def start_server():
        print ("server run")
        Bluetooth_rpi.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        Bluetooth_rpi.server_sock.bind(("",Bluetooth_rpi.port))
        Bluetooth_rpi.server_sock.listen(1)

        Bluetooth_rpi.client_sock,address = Bluetooth_rpi.server_sock.accept()
        print ("Accepted connection from " + str(address))

    def receiveMessages():
      Bluetooth_rpi.data = Bluetooth_rpi.client_sock.recv(1024)
      print ("received", Bluetooth_rpi.data)
      
    def sendMessage():
      Bluetooth_rpi.sock.send(Globale.data_to_send())
      #Bluetooth_rpi.sock.send("joy:"+ str(Globale.joystick_current_value))
      
    def lookUpNearbyBluetoothDevices():
      nearby_devices = bluetooth.discover_devices()
      for bdaddr in nearby_devices:
        print (str(bluetooth.lookup_name( bdaddr )) + " [" +bdaddr+ "]")

    def run_server():
        Bluetooth_rpi.start_server()
        while True:
            Bluetooth_rpi.receiveMessages()
        
    def run_client():
        while True:
            try:
                Bluetooth_rpi.connection()
                while True:
                    Bluetooth_rpi.sendMessage()
                    time.sleep(0.01)
            except:
                print("Connection refused")
                time.sleep(0.1)
                
    def run_client1():
        Bluetooth_rpi.connection()
        while True:
            Bluetooth_rpi.sendMessage()
            time.sleep(0.2)
    
    def cleanup():
        Bluetooth_rpi.client_sock.close()
        Bluetooth_rpi.server_sock.close()
        Bluetooth_rpi.sock.close()


