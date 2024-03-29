from web3 import Web3

from perppy.msg.amm import Amm
from perppy.msg.trader import Trader
from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.msg.portfolio import Portfolio
from perppy.utils.provider import Web3ProviderFactory
from perppy.msg.event.position_changed import PositionChanged
from perppy.utils.constants import get_network_url, ETH_DECIMALS


class QueryConnector:
    """
    QueryConnector acts as a client to query
    exchange data from perp.exchange
    """
    def __init__(self, network: str = 'production'):
        """
        Create a new QueryConnector object.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ['production', 'staging']:
            raise ValueError(f"Invalid network {network}, should be 'production' or 'staging'")
        self.network = network

    def get_position_changes(
        self,
        trader: str = None,
        pair: str = None,
        block_limit: int = 5,
    ):
        """
        Fetches recent position changes on the given network.

        :param trader: Address of a trader
        :param pair: Name of AMM pair
        :param block_limit: Number of blocks from latest till which positions to be fetch
        """
        w3_provider = Web3ProviderFactory().get_layer2_provider(self.network)
        addr = MetaData().get_layer2_contract('ClearingHouse', network=self.network)
        abi  = AbiFactory().get_contract_abi('ClearingHouse')

        block_number: int = w3_provider.eth.getBlock('latest').number
        contract = w3_provider.eth.contract(address=addr, abi=abi)
        filter = contract.events.PositionChanged.createFilter(
            fromBlock=block_number-block_limit,
            toBlock=block_number
        )

        event_msgs = []
        for event in filter.get_all_entries():
            event_msg = PositionChanged(event, self.network)
            event_msgs.append(event_msg)
        return event_msgs

    def get_trader_portfolio(
        self,
        trader: str,
    ):
        """
        Fetches the portfolio information of a trader.

        :param trader: Address of a trader
        """
        w3_provider_layer1 = Web3ProviderFactory().get_layer1_provider(self.network)
        w3_provider_layer2 = Web3ProviderFactory().get_layer2_provider(self.network)

        layer1_usdc_addr = Web3.toChecksumAddress(MetaData().get_layer1_contract('usdc', network=self.network))
        layer1_usdc_abi  = AbiFactory().get_contract_abi('usdc')
        layer1_usdc_contract = w3_provider_layer1.eth.contract(address=layer1_usdc_addr, abi=layer1_usdc_abi)
        layer1_balance = layer1_usdc_contract.functions.balanceOf(trader).call() / 10**layer1_usdc_contract.functions.decimals().call()

        layer2_usdc_addr = MetaData().get_layer2_contract('usdc', network=self.network)
        layer2_usdc_abi  = AbiFactory().get_contract_abi('usdc')
        layer2_usdc_contract = w3_provider_layer2.eth.contract(address=layer2_usdc_addr, abi=layer2_usdc_abi)
        layer2_balance = layer2_usdc_contract.functions.balanceOf(trader).call() / 10**layer2_usdc_contract.functions.decimals().call()

        insurance_fund_addr = MetaData().get_layer2_contract('InsuranceFund', network=self.network)
        insurance_fund_abi  = AbiFactory().get_contract_abi('InsuranceFund')
        insurance_fund_contract = w3_provider_layer2.eth.contract(address=insurance_fund_addr, abi=insurance_fund_abi)

        portfolios = []
        for amm_addr in insurance_fund_contract.functions.getAllAmms().call():
            portfolio = Portfolio(amm_addr, trader, self.network)
            if portfolio is None:
                continue
            portfolios.append(portfolio)
        trader_portfolio = Trader(layer1_balance, layer2_balance, portfolios)
        return trader_portfolio

    def get_all_amms(
        self,
    ):
        """
        Fetches the information of all available AMM pairs.
        """
        w3_provider_layer2 = Web3ProviderFactory().get_layer2_provider(self.network)

        insurance_fund_addr = MetaData().get_layer2_contract('InsuranceFund', network=self.network)
        insurance_fund_abi  = AbiFactory().get_contract_abi('InsuranceFund')
        insurance_fund_contract = w3_provider_layer2.eth.contract(address=insurance_fund_addr, abi=insurance_fund_abi)

        amms = []
        for amm_addr in insurance_fund_contract.functions.getAllAmms().call():
            amm = self.get_amm_info(amm_addr)
            amms.append(amm)
        return amms

    def get_amm_info(
        self,
        amm_addr: str,
    ):
        """
        Fetches the information of given AMM pairs.

        :pair amm_addr: Address of AMM pair
        """
        return Amm(amm_addr, self.network)
