from aptos_sdk.account import AccountAddress
import uuid


class NftCollection:
    def __init__(self, creator_id, name, description, url):
        self.id = uuid.uuid4()
        self.creator_id = creator_id
        self.name = name
        self.description = description
        self.url = url

    def to_dict(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "name": self.name,
            "description": self.description,
            "url": self.url
        }


class NftAsset:
    def __init__(self, collection_id, owner_id, name, description, url):
        self.id = uuid.uuid4()
        self.collection_id = collection_id
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.url = url

    def to_dict(self):
        return {
            "id": self.id,
            "collection_id": self.collection_id,
            "owner_id": self.owner_id,
            "name": self.name,
            "description": self.description,
            "url": self.url
        }
