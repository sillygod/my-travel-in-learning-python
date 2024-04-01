import base64

import ecdsa

INITIAL_BALANCE = 500


class Wallet:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.key_pair = Wallet.gen_key_pair()
        self.public_key = self.key_pair.get_verifying_key().to_string().hex()

    def __str__(self):
        return f"""
        Wallet -
            public_key: {self.public_key}
            balance: {self.balance}
        """

    @staticmethod
    def gen_key_pair():
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        # private_key = sk.to_string().hex()
        # vk = sk.get_verifying_key()
        # public_key = vk.to_string().hex()
        return sk

        # to get r, s value of signature
        # sigdecode_string(signature, sk.privkey.order)

    def sign(self, data_hash):
        sig = self.key_pair.sign(data_hash.encode("utf-8"))
        return base64.b64encode(sig)
