from multiprocessing import Process, Queue
from request import Helper
import logging

NUM_PROC = 9
START_NONCE = 8031939

if __name__ == '__main__':
    nonce_queue = Queue()
    response_queue = Queue()
    procs = []
    nonce = START_NONCE
    line_counter = 0
    logging.basicConfig(level=logging.INFO)
    
    for _ in range(NUM_PROC):
        p = Process(target=Helper.workOnNonce, args=(nonce_queue, response_queue))
        procs.append(p)
        p.start()

    for _ in range(180):
        nonce_queue.put(nonce)
        nonce += 1

    for _ in range(NUM_PROC):
        nonce_queue.put(None)

    response = response_queue.get()
    while response is not None:
        line_counter += 1
        logging.info(' [' + str(line_counter) + '] Found transaction: ' + str(response))
        response = response_queue.get()
    
    
    