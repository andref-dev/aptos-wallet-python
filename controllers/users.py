from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload
from aptos_sdk.bcs import Serializer

from app_data import AppData
from models.users import User


def create_user(app_data: AppData, name):
    user = User(name)
    # Step needed so this account can interact with this resource later
    app_data.faucet_client.fund_account(user.account.address(), 0)
    app_data.users[str(user.id)] = user
    return user.to_dict()


def set_username(app_data: AppData, user_id, username):
    # Get the user from our 'database'
    user: User = app_data.users.get(user_id)

    # Defines which method we will call
    module = f'{app_data.user_info_address}::user_info'
    function = "set_username"

    # Serializes arguments for the method call
    transaction_arguments = [TransactionArgument(username, Serializer.str)]

    # Creates the method call payload
    payload = EntryFunction.natural(
        module,
        function,
        [],
        transaction_arguments,
    )

    # Sign the transactions
    signed_transaction = app_data.rest_client.create_single_signer_bcs_transaction(
        user.account, TransactionPayload(payload)
    )

    # Submit the transaction to the chain
    tx_hash = app_data.rest_client.submit_bcs_transaction(signed_transaction)
    app_data.rest_client.wait_for_transaction(tx_hash)

    return get_username(app_data, user_id)


def get_username(app_data: AppData, user_id):
    user: User = app_data.users.get(user_id)

    # The resource type is the struct deployed on chain
    # 0x962deab0cc8aaf7df4159c84c5c48c451705908bc7806e144e261cc4c76a65c3::user_info::UserProfile
    resource_type = f'{app_data.user_info_address}::user_info::UserProfile'
    resource = app_data.rest_client.account_resource(
        user.account.address(), resource_type)
    print(resource)

    return resource


def get_all_users(app_data: AppData):
    res = []
    for user in app_data.users.values():
        res.append(user.to_dict())

    return res


def get_user(app_data: AppData, user_id):
    user = app_data.users.get(user_id)
    return user.to_dict()
