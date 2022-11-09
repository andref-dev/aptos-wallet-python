from aptos_sdk.client import RestClient, FaucetClient


class AppData:
    def __init__(self):

        rest_url = "https://fullnode.devnet.aptoslabs.com/v1"
        faucet_url = "https://tap.devnet.prod.gcp.aptosdev.com"

        #rest_url = "http://0.0.0.0:8080/v1"
        #faucet_url = "http://0.0.0.0:8000"

        self.users = {}
        self.nft_collections = {}
        self.nft_assets = {}
        self.rest_client = RestClient(rest_url)
        self.faucet_client = FaucetClient(faucet_url, self.rest_client)
