import socket
import random
from abc import ABC, abstractmethod

from coordinator import Coordinator
from transaction_logger import set_logger


SERV_PORT = 9001

class Server:

    def __init__(self):
        self.serv_addr = ("127.0.0.1", SERV_PORT)
        self.logger = set_logger(self.__class__.__name__)

    @staticmethod
    def _generate_port():
        return random.randint(SERV_PORT, 65535)
    

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(self.serv_addr)
        tcp.listen(1)

        sell = False
        buy = False
        while not buy or not sell:
            conn, addr = tcp.accept()
            msg = conn.recv(1024)
            if msg == b'buy':
                buy = True
                print("buy")
                rand_port = str(self._generate_port())

                conn.send(rand_port.encode())

            if msg == b'sell':
                sell = True
                print("sell")
                rand_port = str(self._generate_port())

                conn.send(rand_port.encode())
            conn.close()



        tcp.close()
