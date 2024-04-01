from typing import List

from .transaction import Transaction


class TransactionPool:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def update_or_add_transaction(self, transaction: Transaction):
        index = None
        tx = None

        for i, t in enumerate(self.transactions):
            if t._id == transaction._id:
                index = i
                tx = t
                break

        # if the transaction exists, replace the original one in the pool
        # or append it to the pool
        if tx:
            self.transactions[index] = tx
        else:
            self.transactions.append(transaction)

    def existing_transaction(self, address) -> Transaction:
        for t in self.transactions:
            if t.input.address == address:
                return t

        return None
