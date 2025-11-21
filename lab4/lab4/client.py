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

        for i in range(6):
            # Get an item, set the price, and connect to the server
            item = self._get_item()
            self._set_price(item["price"])
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(self.serv_addr)

            # Create sell request message and send it to server
            msg = transaction_pb2.Transaction()
            msg.type = 1
            msg.name = item["name"]
            msg.price = self._set_price(item["price"])
            send = msg.SerializeToString()
            self.logger.info(f"Listing item: {item["name"]} for ${msg.price}")
            tcp.send(send)
            port = tcp.recv(1024).decode()
            tcp.close()
            # Run Seller participant
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
        for i in range(6):
            # Connect to server and send a buy request
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(self.serv_addr)
            msg = transaction_pb2.Transaction()
            msg.type = 0
            send = msg.SerializeToString()
            tcp.send(send)
            port = tcp.recv(1024).decode()
            tcp.close()

            # Keep trying to connect until the server is ready to notify about an item for sale
            while True:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.connect(self.serv_addr)

                msg1 = transaction_pb2.Transaction()
                msg1.type = 2
                msg1 = msg1.SerializeToString()
                tcp.send(msg1)
                recv1 = tcp.recv(1024)

                # If connection drops, server is not ready so try to connect again
                if recv1 == b'':
                    continue
                else:
                    break


            msg.ParseFromString(recv1)
            tcp.close()

            # Run Buyer participant
            b = Buyer(1, port, msg)
            b.run()


