from abc import ABC, abstractmethod
import json
import socket
from transaction_logger import set_logger

def read_database():
    with open('auction.json', 'r') as file:
        return json.load(file)

class Participant(ABC):
    def __init__(self, transaction_id, port):
        self.port = port
        self.transaction_id = transaction_id
        self.logger = set_logger(f"2PC:" + self.__class__.__name__)

    def run(self):
        pass

    @abstractmethod
    def vote(self):
        pass

    def commit(self):
        self.logger.info(f"Received global commit for transaction {self.transaction_id}, committing.")

    def abort(self):
        self.logger.info(f"Received global abort for transaction {self.transaction_id}, aborting.")


class Seller(Participant):

    def __init__(self, transaction_id, port):
        super().__init__(transaction_id, port)


    def vote(self):
        pass

    def run(self):

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tcp.bind(("127.0.0.1", int(self.port)))
        tcp.listen(1)

        conn, addr = tcp.accept()
        self.logger.info(f"{self.port}:Accepted connection from coordinator (port {addr[1]}), waiting for vote request.")


class Buyer(Participant):

    def __init__(self, transaction_id, port, item):
        super().__init__(transaction_id, port)

    def vote(self):
        pass

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(("127.0.0.1", int(self.port)))
        self.logger.info(f"{self.port}")
        tcp.listen(1)
        conn, addr = tcp.accept()
        self.logger.info(f"{self.port}:Accepted connection from coordinator (port {addr[1]}), waiting for vote request.")
