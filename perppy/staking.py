import os
from web3 import Web3

from perppy.utils.abi import AbiFactory
from perppy.utils.provider import Web3ProviderFactory


class StakingConnenctor:
    """
        ExecuteConnector acts as a client to stake, unstake
        on perp.exchange
    """
    def __init__(self, private_key_env_var: str, network = 'production'):
        self.network         = network
        self.layer1_provider = Web3ProviderFactory().get_layer1_provider(self.network)
        self.layer2_provider = Web3ProviderFactory().get_layer2_provider(self.network)

        self.layer1_account  = self.layer1_provider.eth.account.privateKeyToAccount(os.environ[private_key_env_var])
        self.layer2_account  = self.layer2_provider.eth.account.privateKeyToAccount(os.environ[private_key_env_var])

    def stake_perp(self):
        pass

    def unstake_perp(self):
        pass