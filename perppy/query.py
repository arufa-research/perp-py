import time

from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.utils.provider import Web3ProviderFactory
from perppy.msg.event.position_changed import PositionChanged
from perppy.utils.constants import get_network_url, ETH_DECIMALS


def get_position_changes(
    trader: str = None,
    pair: str = None,
    block_limit: int = 2,
    network_name: str = 'Homestead'
) -> str:
    w3_provider = Web3ProviderFactory().get_provider(network_name)
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
        event_msg = PositionChanged(event, network_name)
        event_msgs.append(event_msg)
    return event_msgs


def get_portfolio(trader: str):
    pass


def get_amm_info(amm_addr: str, amm_pair: str, short_name: bool = False):
    pass


def verify_function_data(contract_addr: str, byte_code: str):
    pass
