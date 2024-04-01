import base64
import json
import uuid
from datetime import datetime
from hashlib import sha256
from typing import Dict, List, Optional
from uuid import UUID

import ecdsa
from ecdsa import VerifyingKey
from ecdsa.keys import BadSignatureError
from pydantic.main import BaseModel

from .wallet import Wallet


class Input(BaseModel):

    timestamp: float
    amount: int
    address: str
    signature: bytes

    class Config:
        json_encoders = {}


class Output(BaseModel):

    amount: int
    address: str


def uuid_json_convert(obj):
    if isinstance(obj, UUID):
        return obj.hex


class Transaction:
    def __init__(self):
        self._id = uuid.uuid1()
        self.input: Optional[Input] = None
        self.outputs: List[Output] = []

    def __eq__(self, other):
        return (
            self._id == other._id
            and self.input == other.input
            and self.outputs == other.outputs
        )

    def update(self, sender_wallet: Wallet, recipient, amount) -> "Transaction":
        sender_output = None

        for output in self.outputs:
            if output.address == sender_wallet.public_key:
                sender_output = output
                break

        if amount > sender_output.amount:
            raise Exception(f"Amount: {amount} exceeds balance: {sender_output.amount}")

        sender_output.amount = sender_output.amount - amount
        self.outputs.append(Output(amount=amount, address=recipient))
        Transaction.sign(self, sender_wallet)
        return self

    @staticmethod
    def to_dict(m: BaseModel) -> Dict:
        return m.dict()

    @staticmethod
    def to_list_of_dict(m: List[BaseModel]) -> List[Dict]:
        return [obj.dict() for obj in m]

    @staticmethod
    def new(sender_wallet: Wallet, recipient, amount):
        transaction = Transaction()

        if amount > sender_wallet.balance:
            raise Exception(
                f"Amount: {amount} exceeds balance: {sender_wallet.balance}"
            )

        transaction.outputs.append(
            Output(
                amount=sender_wallet.balance - amount,
                address=sender_wallet.public_key,
            )
        )

        transaction.outputs.append(
            Output(
                amount=amount,
                address=recipient,
            )
        )

        Transaction.sign(transaction, sender_wallet)

        return transaction

    @staticmethod
    def sign(transaction, sender_wallet):
        hashed_data = sha256(
            json.dumps(Transaction.to_list_of_dict(transaction.outputs)).encode("utf-8")
        ).hexdigest()

        transaction.input = Input(
            timestamp=datetime.now().timestamp(),
            amount=sender_wallet.balance,
            address=sender_wallet.public_key,
            signature=sender_wallet.sign(hashed_data),
        )

    @staticmethod
    def verify(transaction) -> bool:
        hashed_data = (
            sha256(
                json.dumps(Transaction.to_list_of_dict(transaction.outputs)).encode(
                    "utf-8"
                )
            )
            .hexdigest()
            .encode("utf-8")
        )
        vk = VerifyingKey.from_string(
            bytes().fromhex(transaction.input.address), curve=ecdsa.SECP256k1
        )
        try:
            sig = base64.b64decode(transaction.input.signature)
            return vk.verify(sig, hashed_data)
        except BadSignatureError:
            return False
