import json
import socket
import random
import transaction_pb2
from abc import ABC, abstractmethod

from participant import Buyer, Seller
from transaction_logger import set_logger


N_ITEMS = 6
SERV_PORT = 9001

class Client(ABC):

    def __init__(self):
        self.serv_addr = ("127.0.0.1", SERV_PORT)
        self.logger = set_logger(self.__class__.__name__)

    @abstractmethod
    def run(self):
        pass


class SellerClient(Client):
    def __init__(self):
        super().__init__()

    def run(self):

        item = self._get_item()
        self._set_price(item["price"])
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(self.serv_addr)
        msg = transaction_pb2.Transaction()
        msg.type = 1
        msg.name = item["name"]
        msg.price = self._set_price(item["price"])
        send = msg.SerializeToString()
        self.logger.info(f"Listing item: {item["name"]} for ${item["price"]} (item 1/6)")
        tcp.send(send)
        port = tcp.recv(1024).decode()
        self.logger.info(f"Connection from ('127.0.0.1',{port})")
        tcp.close()
        s = Seller(1, port)
        s.run()

    @staticmethod
    def _get_item():
        with open('auction.json', 'r') as file:
            return random.choice(json.load(file))

    @staticmethod
    def _set_price(price):
        return int(price * (1 + random.gauss(0, 0.1)))

class BuyerClient(Client):
    def __init__(self):
        super().__init__()

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(self.serv_addr)
        msg = transaction_pb2.Transaction()
        msg.type = 0
        send = msg.SerializeToString()
        tcp.send(send)
        port = tcp.recv(1024).decode()
        tcp.close()
        self.logger.info(f"Connection from ('127.0.0.1',{port})")
        # tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp.connect(self.serv_addr)
        # packet = tcp.recv(1024)
        # msg.ParseFromString(packet)
        # self.logger.info(msg)
        b = Buyer(1, port, 1)
        b.run()


