import json
import random
import socket
import transaction_pb2

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

        # Connect to both Participants
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(("127.0.0.1", int(self.ports["buyer"])))
        tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp1.connect(("127.0.0.1", int(self.ports["seller"])))

        # Receive commit/abort message from seller
        msg = transaction_pb2.Transaction()
        packet = tcp1.recv(1024)
        msg.ParseFromString(packet)



        # If it is commit
        if msg.type == 3:
            self.logger.info(f"Participant 1 (port {int(self.ports["seller"])}) voted to commit.")

            # Receive commit/abort from buyer
            packet = tcp.recv(1024)
            msg.ParseFromString(packet)
            ack = transaction_pb2.Transaction()

            # If it is commit, both have commited so send global commit
            if msg.type == 3:
                self.logger.info(f"Participant 0 (port {int(self.ports["buyer"])}) voted to commit.")
                self.logger.info("All participants voted to commit, sending global commit.")
                tcp.send(msg.SerializeToString())

                # Receive both acks
                packet = tcp.recv(1024)
                ack.ParseFromString(packet)
                if ack.type == 5:
                    self.logger.info(f"Received acknowledgment from participant (port {int(self.ports["buyer"])}).")
                else:
                    self.logger.info("fail")
                tcp1.send(msg.SerializeToString())
                packet = tcp1.recv(1024)
                ack.ParseFromString(packet)
                if ack.type == 5:
                    self.logger.info(f"Received acknowledgment from participant (port {int(self.ports["seller"])}).")
                    packet = tcp.recv(1024)
                    msg.ParseFromString(packet)
                    self._save_transaction(msg.name, msg.price, True)
                    self.logger.info(f"Saving transaction result: item={msg.name}, price={msg.price}, success=True")
                else:
                    self.logger.info("fail")


            # Same thing as commit but if the buyer aborts
            else:
                self.logger.info(f"Participant 0 (port {int(self.ports["buyer"])}) voted to abort.")
                self.logger.info("Not all participants voted to commit, sending global abort.")
                tcp.send(msg.SerializeToString())
                packet = tcp.recv(1024)
                ack.ParseFromString(packet)
                if ack.type == 5:
                    self.logger.info(f"Received acknowledgment from participant (port {int(self.ports["buyer"])}).")
                else:
                    self.logger.info("fail")
                tcp1.send(msg.SerializeToString())
                packet = tcp1.recv(1024)
                ack.ParseFromString(packet)
                if ack.type == 5:
                    self.logger.info(f"Received acknowledgment from participant (port {int(self.ports["seller"])}).")
                    packet = tcp.recv(1024)
                    msg.ParseFromString(packet)
                    self._save_transaction(msg.name, msg.price, False)
                    self.logger.info(f"Saving transaction result: item={msg.name}, price={msg.price}, success=Fail")
                else:
                    self.logger.info("fail")
        # Seller will never abort so this can be a pass
        else:
            pass


        tcp.close()
        tcp1.close()







