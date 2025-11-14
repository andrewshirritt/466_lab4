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
        self.logger.info(f"64818:Accepted connection from coordinator (port {self.port}), waiting for vote request.")


class Buyer(Participant):

    def __init__(self, transaction_id, port, item):
        super().__init__(transaction_id, port)

    def vote(self):
        pass

    def run(self):
        self.logger.info(f"64818:Accepted connection from coordinator (port {self.port}), waiting for vote request.")
