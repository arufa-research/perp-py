import os
from web3 import Web3

from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.msg.staking import StakingStats
from perppy.utils.provider import Web3ProviderFactory


class StakingConnector:
    """
        StakingConnector acts as a client to stake, unstake
        on perp.exchange and get current staking information
    """
    def __init__(self, private_key_env_var: str = None, network = 'production'):
        """
        Create a new StakingConnector object.

        :param private_key_env_var: environment variable that stores your private key
        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        self.network         = network
        self.layer1_provider = Web3ProviderFactory().get_layer1_provider(self.network)

        if private_key_env_var is not None:
            self.layer1_account  = self.layer1_provider.eth.account.privateKeyToAccount(os.environ[private_key_env_var])

    def get_current_stats(self):
        """
        Fetch staking rewards related information.
        """
        perp_reward_vesting_addr     = MetaData().get_layer1_contract('PerpStakingRewardVesting', network=self.network)
        perp_reward_no_vesting_addr  = MetaData().get_layer1_contract('PerpStakingRewardNoVesting', network=self.network)
        perp_reward_vesting_abi  = AbiFactory().get_contract_abi('PerpRewardVesting')
        perp_reward_vesting_contract = self.layer1_provider.eth.contract(address=perp_reward_vesting_addr, abi=perp_reward_vesting_abi)

        seed_allocation = perp_reward_vesting_contract.functions.getLengthOfMerkleRoots().call()

        perp_token_addr = Web3.toChecksumAddress(MetaData().get_layer1_contract('perp', network=self.network))
        perp_token_abi  = AbiFactory().get_contract_abi('ERC20ViewOnly')
        perp_token_contract = self.layer1_provider.eth.contract(address=perp_token_addr, abi=perp_token_abi)

        governance_addr = MetaData().get_layer1_contract('rewardGovernance', network=self.network)
        perp_balance = perp_token_contract.functions.balanceOf(governance_addr).call()

        vesting_allowance   = perp_token_contract.functions.allowance(governance_addr, perp_reward_vesting_addr).call()
        novesting_allowance = perp_token_contract.functions.allowance(governance_addr, perp_reward_no_vesting_addr).call()

        staking_stats = StakingStats(seed_allocation, perp_balance, vesting_allowance, novesting_allowance)
        return staking_stats

    # def stake_perp(self):
    #     pass

    # def unstake_perp(self):
    #     pass