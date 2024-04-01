from .transaction import Transaction
from .transaction_pool import TransactionPool
from .wallet import Wallet


def create_transaction(
    wallet: Wallet, recipient, amount, transaction_pool: TransactionPool
):
    if amount > wallet.balance:
        raise Exception(f"Amount: {amount} exceeds balance: {wallet.balance}")

    tx = transaction_pool.existing_transaction(wallet.public_key)

    if tx:
        tx.update(wallet, recipient, amount)
    else:
        tx = Transaction.new(wallet, recipient, amount)
        transaction_pool.update_or_add_transaction(tx)

    return tx
