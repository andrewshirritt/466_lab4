from client import BuyerClient, SellerClient
from server import Server
import concurrent.futures
import random

SEED = 839672

if __name__ == "__main__":

    random.seed(SEED)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        communicators = [Server(), BuyerClient(), SellerClient()]
        executor.map(lambda x: x.run(), communicators)

