from abc import ABC, abstractmethod
import json
import socket
import transaction_pb2
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
        self.tcp = None
        self.conn = None


    def vote(self):

        msg = transaction_pb2.Transaction()
        msg.type = 3
        self.logger.info(msg)
        sendmsg = msg.SerializeToString()
        self.conn.send(sendmsg)

    def run(self):

        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tcp.bind(("127.0.0.1", int(self.port)))
        self.tcp.listen(1)

        self.conn, addr = self.tcp.accept()
        self.logger.info(f"{self.port}:Accepted connection from coordinator (port {addr[1]}), waiting for vote request.")
        self.vote()
        msg = transaction_pb2.Transaction()
        packet = self.conn.recv(1024)
        msg.ParseFromString(packet)
        if msg.type == 3:
            self.commit()
            ack = transaction_pb2.Transaction()
            ack.type = 5
            self.conn.send(ack.SerializeToString())
        else:
            self.abort()
            ack = transaction_pb2.Transaction()
            ack.type = 5
            self.conn.send(ack.SerializeToString())


class Buyer(Participant):

    def __init__(self, transaction_id, port, item):
        super().__init__(transaction_id, port)
        self.item = item
        self.tcp = None
        self.conn = None

    def vote(self):
        with open('auction.json', 'r') as file:
            data = json.load(file)
            for item in data:
                if item["name"] == self.item.name:
                    market = item


        msg = transaction_pb2.Transaction()

        if self.item.price >= market["price"]:
            msg.type = 3
        else:
            msg.type = 4


        sendmsg = msg.SerializeToString()
        self.conn.send(sendmsg)

    def run(self):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind(("127.0.0.1", int(self.port)))
        self.tcp.listen(1)
        self.conn, addr = self.tcp.accept()
        self.logger.info(f"{self.port}:Accepted connection from coordinator (port {addr[1]}), waiting for vote request.")
        self.logger.info(self.item.price)
        self.vote()
        msg = transaction_pb2.Transaction()
        packet = self.conn.recv(1024)
        msg.ParseFromString(packet)
        if msg.type == 3:
            self.commit()
            ack = transaction_pb2.Transaction()
            ack.type = 5
            self.conn.send(ack.SerializeToString())
            self.conn.send(self.item.SerializeToString())
        else:
            self.abort()
	    ack = transaction_pb2.Transaction()
            ack.type = 5
            self.conn.send(ack.SerializeToString())
            self.conn.send(self.item.SerializeToString())
