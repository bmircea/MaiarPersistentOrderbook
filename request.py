import requests
import json
import time
import smart_contract_addresses

class Transaction:
    tx_hash = ''
    def __init__(self, hash):
        self.tx_hash = hash
        print('Transaction created', hash)

    @classmethod
    def get_tx_by_hash(self):
        get_tx_by_hash_url = 'https://gateway.elrond.com/transaction/{0}'
        r = requests.get(get_tx_by_hash_url.format(self.tx_hash))
        if (r.status_code == 200):
            pass

        

class Block:
    block_hash = ''
    block_nonce = 0
    txs_num = ''
    txs = []
    sc_address_list = smart_contract_addresses.smart_contracts.values()

    def __init__(self, json_dump):
        response = json.loads(json_dump)
        if (response['code'] == 'successful'):
            data = response['data']
            self.block_hash = data['block']['hash']
            self.txs_num = data['block']['numTxs']
            self.block_nonce = data['block']['nonce']
            Block.get_txs_hash_only(self.txs, data['block']['miniBlocks'])
            #print('Created block')
    
    @staticmethod
    def query_block_hash_only(nonce):
        get_block_by_nonce_url = 'https://gateway.elrond.com/block/{0}/by-nonce/{1}?withTxs=True'
        tx_list = []
        for i in range(3):
            r = requests.get(get_block_by_nonce_url.format(str(i), str(nonce)))
            if (r.status_code == 200):
                resp = json.loads(r.text)
                if (resp['code'] == 'successful'):
                    mb = resp['data']['block']['miniBlocks']
                    for item in Block.query_txs_hash_only(mb):
                        tx_list.append(item)
            time.sleep(0.1)
        return tx_list

    @staticmethod
    def query_txs_hash_only(miniblocks):  # Only get the hash of the transactions
        hash_list = []
        for block in miniblocks:                 # from blocks. Need to filter afterwards.
            for tx in block['transactions']:
                hash_list.append((tx['hash'], tx['receiver']))
        return Block.filter_txs(hash_list)

    @classmethod
    def filter_txs(self, hash_list):    # Filter txs by receiver (smart contracts only)
        sc_address_list = self.sc_address_list 
        tx_list = []
        for hash in hash_list:
            if hash[1] in sc_address_list:
                tx_list.append(hash[0])
        return tx_list
    """
    def __init__(self, json_dump):
        response = json.loads(json_dump)
        if (response['code'] == 'successful'):
            data = response['data']
            self.block_nonce = data['block']['nonce']
            self.block_hash = data['block']['hash']
            self.txs_num = data['block']['numTxs']
            Block.get_txs(self.txs, data['block']['miniBlocks'])
            print('Created block')

    @staticmethod
    def get_txs(tx_list, miniblocks):
        #txs = miniblocks['transactions']
        for block in miniblocks:
            for tx in block['transactions']:
                (print(json.dumps(tx, indent=4)))
        

    @staticmethod
    def query_blocks(blocks_list, start_nonce):
        get_block_by_nonce_url = 'https://gateway.elrond.com/block/{0}/by-nonce/{1}?withTxs=True'
        nonce = start_nonce
        for _ in range(1):
            for i in range(3):
                r = requests.get(get_block_by_nonce_url.format(str(i), str(nonce)))
                if (r.status_code == 200):
                    blocks_list.append(Block(r.text))
                time.sleep(0.1)
            nonce += 1
    """

class Network:
    network_config_url = 'https://gateway.elrond.com/network/config'
    def networkConfig(self):
        r = requests.get(self.network_config_url)
        return r.json()



#blocks = []
#start_nonce = 8031939
#for _ in range(2):
#    resp = Block.query_block_hash_only(start_nonce)
#    start_nonce += 1
#    print(resp)

if __name__ == '__main__':
    print('Class file. Do not run directly!')
    exit(-1)