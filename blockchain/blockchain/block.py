from hashlib import sha256
from datetime import datetime

DIFFICULTY = 3
MINE_RATE = 3000

class Block:

    def __init__(self, timestamp, lastHash, hash, data, nonce, difficulty):
        self.timestamp: float = timestamp
        self.lastHash: str = lastHash
        self.hash_value: str = hash
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty or DIFFICULTY

    def __str__(self):
        return (f"\nblock - \n"
                f"\tTimestamp: {self.timestamp}\n"
                f"\tLast Hash: {self.lastHash}\n"
                f"\tHash: {self.hash_value}\n"
                f"\tNonce: {self.nonce}\n"
                f"\tDifficulty: {self.difficulty}\n"
                f"\tData: {self.data}\n")

    def __eq__(self, other: 'Block'):
        return self.timestamp == other.timestamp and self.lastHash ==  other.lastHash and self.hash_value == other.hash_value and self.data == other.data and self.nonce == other.nonce

    @staticmethod
    def genesis() -> 'Block':
        tx = datetime(1991, 2, 11).timestamp()
        return Block(tx, '-----', 'f1r57-h45h', [], 0, DIFFICULTY)

    @staticmethod
    def mine_block(last_block: 'Block', data) -> 'Block':
        nonce = 0
        last_hash = last_block.hash_value
        timestamp = datetime.now().timestamp()
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        hash = Block.hash(timestamp, last_hash, data, nonce, difficulty)

        while hash[:difficulty] != '0'*difficulty:
            nonce = nonce + 1
            timestamp = datetime.now().timestamp()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = Block.hash(timestamp, last_hash, data, nonce, difficulty)

        return Block(timestamp, last_hash, hash, data, nonce, difficulty)

    @staticmethod
    def hash(timestamp, last_hash, data, nonce, difficulty) -> str:
        return sha256(f"{timestamp}{last_hash}{data}{nonce}{difficulty}".encode('utf-8')).hexdigest()

    @staticmethod
    def adjust_difficulty(last_block: 'Block', timestamp) -> int:
        difficulty = last_block.difficulty
        difficulty = difficulty + 1 if last_block.timestamp + MINE_RATE > timestamp else difficulty - 1
        return difficulty

    @staticmethod
    def blockhash(block: 'Block'):
        return Block.hash(block.timestamp, block.lastHash, block.data, block.nonce, block.difficulty)
