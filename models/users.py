from aptos_sdk.account import Account
import uuid


class User:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.account = Account.generate()

    def to_dict(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "address": self.account.address().hex(),
            "private_key": self.account.private_key.hex()
        }
        return dict
