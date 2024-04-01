from blockchain.chain import BlockChain
from datetime import datetime
from blockchain.block import Block

def test_create_block():

    first_block = Block.genesis()
    print(first_block)

    second_block = Block.mine_block(first_block, "songla gan")
    print(second_block)


def test_block_chain():

    bc = BlockChain()
    data = "songoh"
    bc.add_block(data)

    assert bc.blocks[-1].data == data

    assert bc.is_valid_chain(bc) is True

    bc.blocks[1].data = 'tampered songoh'
    assert bc.is_valid_chain(bc) is False

def test_replace_block_chain():

    bc = BlockChain()
    data = "songaoh"
    bc.add_block(data)
    bc2 = BlockChain()
    bc2.add_block("foo")
    bc2.add_block("goo")

    bc.replace_chain(bc2)

    assert bc.blocks == bc2.blocks

    # make bc's blocks are longer than bc2' blocks' length
    # so the replacement will not happen

    bc.add_block("yo")
    bc.replace_chain(bc2)

    assert bc.blocks != bc2.blocks


def test_block_difficulty():
    from blockchain.block import DIFFICULTY
    bc = BlockChain()
    bc.add_block("ok")
    block = bc.blocks[-1]
    assert block.hash_value[:block.difficulty] == '0'*block.difficulty