from app_data import AppData
from models.nfts import NftAsset, NftCollection
from models.users import User


def create_collection(app_data: AppData, creator_id, name, description, url):
    owner: User = app_data.users.get(creator_id)
    tx_hash = app_data.rest_client.create_collection(
        owner.account, name, description, url)
    app_data.rest_client.wait_for_transaction(tx_hash)

    coll = NftCollection(creator_id, name, description, url)

    app_data.nft_collections[str(coll.id)] = coll

    return coll.to_dict()


def get_all_collections(app_data: AppData):
    res = []
    for coll in app_data.nft_collections.values():
        res.append(coll.to_dict())
    return res


def get_collection_data(app_data: AppData, coll_id):
    coll = app_data.nft_collections.get(coll_id)
    res = coll.to_dict()

    creator: User = app_data.users.get(coll.creator_id)

    data = app_data.rest_client.get_collection(
        creator.account.address(), coll.name)

    res["chain_data"] = data

    return res


def create_token(app_data: AppData, coll_id, owner_id, name, description, url, amount):
    coll: NftCollection = app_data.nft_collections.get(coll_id)
    creator: User = app_data.users.get(coll.creator_id)
    owner: User = app_data.users.get(owner_id)

    # First we create the new token
    tx_hash = app_data.rest_client.create_token(
        creator.account, coll.name, name, description, amount, url, 0)
    app_data.rest_client.wait_for_transaction(tx_hash)

    asset = NftAsset(str(coll.id), owner_id, name, description, url)
    app_data.nft_assets[str(asset.id)] = asset

    # Then we transfer it to the owner (if not the same as creator)
    if str(owner.id) != str(creator.id):
        tx_hash = app_data.rest_client.direct_transfer_token(
            creator.account, owner.account, creator.account.address(), coll.name, name, 0, amount)
        app_data.rest_client.wait_for_transaction(tx_hash)

    return asset.to_dict()


def get_all_tokens(app_data: AppData):
    res = []
    for asset in app_data.nft_assets.values():
        res.append(asset.to_dict())
    return res


def get_token_balance(app_data: AppData, token_id, owner_id):
    token: NftAsset = app_data.nft_assets.get(token_id)
    coll: NftCollection = app_data.nft_collections.get(token.collection_id)
    owner: User = app_data.users.get(owner_id)
    creator: User = app_data.users.get(coll.creator_id)
    token_balance = app_data.rest_client.get_token_balance(
        owner.account.address(), creator.account.address(), coll.name, token.name, 0)

    return {
        "balance": token_balance,
    }


def get_token_data(app_data: AppData, token_id):
    token: NftAsset = app_data.nft_assets.get(token_id)
    coll: NftCollection = app_data.nft_collections.get(token.collection_id)
    creator: User = app_data.users.get(coll.creator_id)

    res = token.to_dict()

    data = app_data.rest_client.get_token_data(
        creator.account.address(), coll.name, token.name, 0)

    res["chain_data"] = data

    return res


def transfer_token(app_data: AppData, token_id, sender_id, receiver_id, amount):
    token: NftAsset = app_data.nft_assets.get(token_id)
    coll: NftCollection = app_data.nft_collections.get(token.collection_id)
    creator: User = app_data.users.get(coll.creator_id)
    sender: User = app_data.users.get(sender_id)
    receiver: User = app_data.users.get(receiver_id)

    tx_hash = app_data.rest_client.direct_transfer_token(
        sender.account, receiver.account, creator.account.address(), coll.name, token.name, 0, amount)
    app_data.rest_client.wait_for_transaction(tx_hash)

    sender_balance = app_data.rest_client.get_token_balance(
        sender.account.address(), creator.account.address(), coll.name, token.name, 0)
    receiver_balance = app_data.rest_client.get_token_balance(
        receiver.account.address(), creator.account.address(), coll.name, token.name, 0)

    return {
        "sender_id": sender.id,
        "sender_balance": sender_balance,
        "receiver_id": receiver.id,
        "receiver_balance": receiver_balance,
    }
