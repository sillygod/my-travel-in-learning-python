from typing import List, Dict 
from .block import Block


class BlockChain:

    def __init__(self):
        self.blocks = [Block.genesis()]

    def __len__(self):
        return len(self.blocks)

    @staticmethod
    def from_blocks(blocks: List[Block]):
        bc =  BlockChain()
        bc.blocks = blocks
        return bc

    def to_json(self) -> List[Dict]:
        return [block.__dict__ for block in self.blocks]

    def add_block(self, data):
        last_block = self.blocks[-1]
        block = Block.mine_block(last_block, data)
        self.blocks.append(block)
        return block

    def is_valid_chain(self, chain: 'BlockChain') -> bool:

        if chain.blocks[0] != Block.genesis():
            return False

        last_block = chain.blocks[0]

        for block in chain.blocks[1:]:

            if block.lastHash != last_block.hash_value or block.hash_value != Block.blockhash(block):
                return False

            last_block = block


        return True

    def replace_chain(self, chain: 'BlockChain'):
        if len(chain) < len(self):
            print("received chain is not longer than the current chain")
            return

        elif not self.is_valid_chain(chain):
            print("received chain is not valid")
            return

        self.blocks = chain.blocks.copy()
