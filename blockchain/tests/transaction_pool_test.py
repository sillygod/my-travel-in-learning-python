import json

from wallet.transaction import Transaction, uuid_json_convert
from wallet.transaction_pool import TransactionPool
from wallet.wallet import Wallet


def test_transaction_pool():
    tp = TransactionPool()
    w = Wallet()

    tx = Transaction.new(w, "songa-al-ancha", 30)
    tp.update_or_add_transaction(tx)

    for t in tp.transactions:
        if t._id == tx._id:
            assert t == tx

    old_tx_str = json.dumps(tx.__dict__, default=uuid_json_convert)
    new_tx = tx.update(w, "songa-222-al-ancha", 40)
    tp.update_or_add_transaction(new_tx)

    for t in tp.transactions:
        if t._id == new_tx._id:
            assert old_tx_str != json.dumps(new_tx.__dict__, default=uuid_json_convert)
