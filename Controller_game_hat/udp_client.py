import socket
import time
from globales import *

class Udp_client:

    def __init__(self):
        self.addrPort = ("192.168.43.124", 9999)
        self.bufferSize = 1024
        # Create UDP socket client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendMessage(self):
        while True:
            msg_to_send = str.encode(Globale.data_to_send())
            self.sock.sendto(msg_to_send, self.addrPort)
            time.sleep(0.01)

    def receiveMessages(self):
        while True:
            receive_msg = self.sock.recvfrom(self.bufferSize)
            print(receive_msg[0])
            Globale.parse_feedback(receive_msg[0])