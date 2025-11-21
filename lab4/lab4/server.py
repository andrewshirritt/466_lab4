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
        # Have an id for each transaction
        tid = 0
        for i in range(6):
            # Listen for clients
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.bind(self.serv_addr)
            tcp.listen(1)
            self.logger.info("Server listening on ('127.0.0.1', 9001)")
            ports = {}

            # Loop until both buyer and seller connect
            sell = False
            buy = False
            msg = transaction_pb2.Transaction()
            while not buy or not sell:
                conn, addr = tcp.accept()

                packet = conn.recv(1024)
                msg.ParseFromString(packet)

                # If it is the buyer again, ignore. Will deal with it later
                if msg.type == 2:
                    conn.close()

                # Buy request, create port for buyer
                if msg.type == 0:
                    buy = True
                    self.logger.info(f"Connection from {addr}")

                    rand_port1 = str(self._generate_port())
                    ports["buyer"] = rand_port1
                    conn.send(rand_port1.encode())
                    conn.close()

                # Sell request, create port for seller and receive the item to sell
                if msg.type == 1:
                    price = msg.price
                    name = msg.name
                    self.logger.info(f"Connection from {addr}")
                    self.logger.info(f"Received request to auction item: {name}")

                    sell = True

                    rand_port2 = str(self._generate_port())
                    ports["seller"] = rand_port2
                    conn.send(rand_port2.encode())
                    conn.close()

            # Ready for next transaction
            tid += 1

            # Notify buyer of item for sale
            conn, addr = tcp.accept()
            msg.price = price
            msg.name = name
            conn.send(msg.SerializeToString())
            conn.close()

            self.logger.info(f"Initiating transaction id {tid} with 1 buyers.")

            tcp.close()
            # Run the Coordinator
            c = Coordinator(ports, tid)
            c.run()


