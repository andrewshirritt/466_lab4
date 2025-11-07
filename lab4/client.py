import json
import socket
import random
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
        tcp.send(b'sell')
        port = tcp.recv(1024)
        print(port)
        tcp.close()

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
        tcp.send(b'buy')
        port = tcp.recv(1024)
        print(port)
        tcp.close()
