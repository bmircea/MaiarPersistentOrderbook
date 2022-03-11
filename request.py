import requests
import json
import time
import smart_contract_addresses
import base64



class Helper(object):
    GET_TX_BY_HASH_URL = 'https://gateway.elrond.com/transaction/{0}?withResults=True'
    GET_BLOCK_BY_NONCE_URL = 'https://gateway.elrond.com/block/{0}/by-nonce/{1}?withTxs=True'
    
    @classmethod
    def getTxByHash(self, hash):
        r = requests.get(self.GET_TX_BY_HASH_URL.format(hash))
        if (r.status_code == 200):
            pass

    @classmethod
    def queryBlockHashOnly(self, nonce):
        tx_list = []
        for i in range(3):
            r = requests.get(self.GET_BLOCK_BY_NONCE_URL.format(str(i), str(nonce)))
            if (r.status_code == 200):
                resp = json.loads(r.text)
                if (resp['code'] == 'successful'):
                    mb = resp['data']['block']['miniBlocks']
                    for item in Helper.queryTxsHashOnly(mb):
                        tx_list.append(item)
            time.sleep(0.1)
        return tx_list

    @staticmethod
    def queryTxsHashOnly(miniblocks):  # Only get the hash of the transactions
        hash_list = []
        for block in miniblocks:                 # from blocks. Need to filter afterwards.
            for tx in block['transactions']:
                hash_list.append((tx['hash'], tx['receiver']))
        return Helper.filterTxs(hash_list)

    @staticmethod
    def filterTxs(hash_list):    # Filter txs by receiver (smart contracts only)
        sc_address_list = smart_contract_addresses.smart_contracts.values()
        tx_list = []
        for hash in hash_list:
            if hash[1] in sc_address_list:
                tx_list.append(hash[0])
        return tx_list

    @staticmethod
    def workOnNonce(nonce_queue, response_queue):
        nonce = nonce_queue.get()
        while nonce is not None:
            response = Helper.queryBlockHashOnly(nonce)
            if len(response) > 0:
                for item in response:
                    response_queue.put(item)
            nonce = nonce_queue.get()
        response_queue.put(None)

    @staticmethod
    def decode(data):
        # Decode 'data' string from tx - ESDTTransfer@A@B
        # where A - Asset name (string) hex-encoded
        # and B - Asset qty (BigUInt) hex-encoded 

        action, asset, qty = data.split('@')
        qty = int(qty, 16) # Hex to Dec 
        asset = bytes.fromhex(asset).decode('ascii') # Hex to String
        
        print(action, asset, qty)


if __name__ == '__main__':
    print('Helper file. Do not run directly!')
    #exit(-1)
    Helper.decode("ESDTTransfer@524944452d376431386539@05fd3ac726aa0d6f0b")