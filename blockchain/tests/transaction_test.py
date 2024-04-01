import pytest

from wallet import transaction, wallet


def test_transaction():
    w = wallet.Wallet()
    amount = 50
    recipient = "songa address"
    tx = transaction.Transaction.new(w, recipient, amount)

    for output in tx.outputs:
        if output.address == w.public_key:
            assert output.amount == w.balance - amount

    # outputs the amount added to the recipient
    for output in tx.outputs:
        if output.address == recipient:
            assert output.amount == amount

    assert tx.input.amount == w.balance

    assert transaction.Transaction.verify(tx) is True

    # let's test updating transaction
    next_amount = 20
    next_recipient = "songa-anza"

    tx.update(w, next_recipient, next_amount)

    for output in tx.outputs:
        if output.address == w.public_key:
            assert output.amount == w.balance - amount - next_amount

    for output in tx.outputs:
        if output.address == next_recipient:
            assert output.amount == next_amount

    # corrupt the tx here
    tx.outputs[0].amount = 20000
    assert transaction.Transaction.verify(tx) is False


def test_transaction_with_insufficient_balance():
    w = wallet.Wallet()
    amount = 50000
    recipient = "songa address"

    with pytest.raises(Exception) as e:
        transaction.Transaction.new(w, recipient, amount)

        assert str(e) == f"Amount: {amount} exceeds balance: {w.balance}"
