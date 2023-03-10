import hashlib
import datetime as date

class Block:
    def __init__(self, data, previous_block_hash):
        self.timestamp = date.datetime.now()
        self.data = data
        self.previous_block_hash = previous_block_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_block_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def add_block(self, data):
        previous_block_hash = self.chain[-1].hash
        new_block = Block(data, previous_block_hash)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.data)
            print("Block Hash: ", block.hash)
            print("Previous Block Hash: ", block.previous_block_hash)
            print("-" * 20)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_block_hash != previous_block.hash:
                return False
        else:
            return True

# Example usage
blockchain = Blockchain()

blockchain.add_block("Transaction Data 1")
blockchain.add_block("Transaction Data 2")

def tamper_data(data, block_index, blockchain: Blockchain):
    for j in range(block_index, len(blockchain.chain)):
        if j < (len(blockchain.chain) - 1):
            current_block = blockchain.chain[j]
            next_block = blockchain.chain[j + 1]

            if j == block_index:
                current_block.data = data
            current_block.hash = current_block.calculate_hash()
            next_block.previous_block_hash = current_block.hash

            blockchain.chain[j] = current_block
            blockchain.chain[j + 1] = next_block
    
    return blockchain
                

blockchain.print_chain()

blockchain = tamper_data("Data 5", 1, blockchain)

print("#" * 100)
blockchain.print_chain()

print(blockchain.is_chain_valid())
