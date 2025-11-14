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
        tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp1.bind(self.serv_addr)
        tcp2.bind(self.serv_addr)
        tcp1.listen(1)
        tcp2.listen(1)
        self.logger.info("Server listening on ('127.0.0.1', 9001)")


        sell = False
        buy = False
        msg = transaction_pb2.Transaction()
        while not buy or not sell:
            conn1, addr1 = tcp1.accept()
            conn2, addr2 = tcp2.accept()


            packet = conn1.recv(1024)
            msg.ParseFromString(packet)


            if msg.type == 0:

                buy = True


                rand_port1 = str(self._generate_port())
                conn1.send(rand_port1.encode())

            if msg.type == 1:
                price = msg.price
                name = msg.name
                self.logger.info(f"Received request to auction item: {name}")

                sell = True

                rand_port2 = str(self._generate_port())
                conn1.send(rand_port2.encode())

            tid = 1





        # conn, addr = tcp.accept()
        msg.price = price
        msg.name = name
        # conn.send(msg.SerializeToString())

        self.logger.info(f"Initiating transaction id {tid} with 1 buyers.")
        conn1.close()
        conn2.close()
        tcp1.close()
        tcp2.close()
