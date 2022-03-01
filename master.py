from multiprocessing import Process, Queue, sharedctypes, Pipe, Barrier
import multiprocessing
from request import Network, Block, Transaction
import ctypes
import numpy

NUM_PROC = 9


def work_on_nonce(nonce_queue, response_queue, b):
    nonce = nonce_queue.get()
    while nonce is not None:
        response = Block.query_block_hash_only(nonce)
        if len(response) > 0:
            for item in response:
                response_queue.put(item)
        nonce = nonce_queue.get()
    response_queue.put(None)
    #b.wait()


if __name__ == '__main__':
    #tx_list = [multiprocessing.Array(ctypes.c_char, '' * 1000) for i in range(3)]
    #tx_list = sharedctypes.RawArray(ctypes.c_char, 64)
    b = Barrier(NUM_PROC + 1)
    nonce_queue = Queue()
    response_queue = Queue()
    procs = []
    for _ in range(NUM_PROC):
        p = Process(target=work_on_nonce, args=(nonce_queue, response_queue, b))
        procs.append(p)
        p.start()

    nonce = 8031939
    for _ in range(180):
        nonce_queue.put(nonce)
        nonce += 1

    for _ in range(NUM_PROC):
        nonce_queue.put(None)

    #b.wait()

    response = response_queue.get()
    while response is not None:
        print(response)
        response = response_queue.get()
    
    
    