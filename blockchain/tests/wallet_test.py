from wallet import wallet
from wallet.transaction_pool import TransactionPool
from wallet.wallet_tx import create_transaction


def test_wallet_create():
    w = wallet.Wallet()
    print(w)


def test_wallet_create_transaction():

    w = wallet.Wallet()
    tp = TransactionPool()
    send_amount = 50
    recipient = "songa-la-223"

    tx = create_transaction(w, recipient, send_amount, tp)
    create_transaction(w, recipient, send_amount, tp)

    for output in tx.outputs:
        if output.address == w.public_key:
            assert output.amount == w.balance - send_amount * 2

    outs = list(filter(lambda x: x.address == recipient, tx.outputs))
    assert len(outs) == 2

    for out in outs:
        assert out.amount == send_amount
