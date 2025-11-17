import json
import random
import socket

from transaction_logger import set_logger

class Coordinator:

    def __init__(self, participant_ports, transaction_id):
        self.logger = set_logger("2PC:" + self.__class__.__name__)
        self.ports = participant_ports
        self.tid = transaction_id

    @staticmethod
    def _save_transaction(name: str, price: int, success: bool):
        data = {
            "item_id": f"{random.getrandbits(16):04x}",
            "name": name,
            "price": price,
            "success": success
        }
        with open("output.json", 'a') as file:
            json.dump(data, file, indent=4)
            file.write("\n")

    def run(self):

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tcp.connect(("127.0.0.1", int(self.ports["buyer"])))
        self.logger.info(self.ports["seller"])
        tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp1.connect(("127.0.0.1", int(self.ports["seller"])))

