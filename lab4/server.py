import socket
import random
import transaction_pb2
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
        self.logger.info("Server listening on ('127.0.0.1', 9001)")
        ports = {}


        sell = False
        buy = False
        msg = transaction_pb2.Transaction()
        while not buy or not sell:
            conn, addr = tcp.accept()

            packet = conn.recv(1024)
            msg.ParseFromString(packet)

            if msg.type == 2:
                conn.close()



            if msg.type == 0:

                buy = True
                self.logger.info(f"Connection from ('127.0.0.1',{addr})")

                rand_port1 = str(self._generate_port())
                ports["buyer"] = rand_port1
                conn.send(rand_port1.encode())
                conn.close()

            if msg.type == 1:
                price = msg.price
                name = msg.name
                self.logger.info(f"Connection from ('127.0.0.1',{addr})")
                self.logger.info(f"Received request to auction item: {name}")

                sell = True

                rand_port2 = str(self._generate_port())
                ports["seller"] = rand_port2
                conn.send(rand_port2.encode())
                conn.close()

            tid = 1





        conn, addr = tcp.accept()
        msg.price = price
        msg.name = name
        self.logger.info(msg)
        conn.send(msg.SerializeToString())
        conn.close()

        self.logger.info(f"Initiating transaction id {tid} with 1 buyers.")

        tcp.close()
        c = Coordinator(ports, tid)
        c.run()
