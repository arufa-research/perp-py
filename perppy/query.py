import time
from web3 import Web3

from perppy.msg.trader import Trader
from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.msg.portfolio import Portfolio
from perppy.utils.provider import Web3ProviderFactory
from perppy.msg.event.position_changed import PositionChanged
from perppy.utils.constants import get_network_url, ETH_DECIMALS


def get_position_changes(
    trader: str = None,
    pair: str = None,
    block_limit: int = 2,
    network: str = 'production'
):
    w3_provider = Web3ProviderFactory().get_layer2_provider(network)
    addr = MetaData().get_layer2_contract('ClearingHouse')
    abi  = AbiFactory().get_contract_abi('ClearingHouse')

    block_number: int = w3_provider.eth.getBlock('latest').number
    contract = w3_provider.eth.contract(address=addr, abi=abi)
    filter = contract.events.PositionChanged.createFilter(
        fromBlock=block_number-block_limit,
        toBlock=block_number
    )

    event_msgs = []
    for event in filter.get_all_entries():
        event_msg = PositionChanged(event, network)
        event_msgs.append(event_msg)
    return event_msgs


def get_trader_portfolio(
    trader: str,
    network: str = 'production'
):
    w3_provider_layer1 = Web3ProviderFactory().get_layer1_provider(network)
    w3_provider_layer2 = Web3ProviderFactory().get_layer2_provider(network)

    layer1_usdc_addr = Web3.toChecksumAddress(MetaData().get_layer1_contract('usdc'))
    layer1_usdc_abi  = AbiFactory().get_contract_abi('usdc')
    layer1_usdc_contract = w3_provider_layer1.eth.contract(address=layer1_usdc_addr, abi=layer1_usdc_abi)
    layer1_balance = layer1_usdc_contract.functions.balanceOf(trader).call() / 10**layer1_usdc_contract.functions.decimals().call()

    layer2_usdc_addr = MetaData().get_layer2_contract('usdc')
    layer2_usdc_abi  = AbiFactory().get_contract_abi('usdc')
    layer2_usdc_contract = w3_provider_layer2.eth.contract(address=layer2_usdc_addr, abi=layer2_usdc_abi)
    layer2_balance = layer2_usdc_contract.functions.balanceOf(trader).call() / 10**layer2_usdc_contract.functions.decimals().call()

    insurance_fund_addr = MetaData().get_layer2_contract('InsuranceFund')
    insurance_fund_abi  = AbiFactory().get_contract_abi('InsuranceFund')
    insurance_fund_contract = w3_provider_layer2.eth.contract(address=insurance_fund_addr, abi=insurance_fund_abi)

    portfolios = []
    for amm_addr in insurance_fund_contract.functions.getAllAmms().call():
        portfolio = Portfolio(amm_addr, trader, network)
        if portfolio is None:
            continue
        portfolios.append(portfolio)
    trader_portfolio = Trader(layer1_balance, layer2_balance, portfolios)
    return trader_portfolio


def get_all_amms(
    network: str = 'production'
):
    pass


def get_amm_info(amm_addr: str, amm_pair: str, short_name: bool = False):
    pass


def verify_function_data(contract_addr: str, byte_code: str):
    pass
