import json
import random
import socket

from transaction_logger import set_logger

class Coordinator:

    def __init__(self, participant_ports, transaction_id):
        self.logger = set_logger("2PC:" + self.__class__.__name__)

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

