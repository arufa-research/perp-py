import time
import datetime as dt
from web3 import Web3
from web3.middleware import local_filter_middleware

from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.utils.constants import get_network_url, ETH_DECIMALS


def get_position_changes(
    trader: str = None,
    pair: str = None,
    block_limit: int = 10,
    network_name: str = 'Homestead'
) -> str:
    w3 = Web3(Web3.HTTPProvider(get_network_url(network_name)))
    w3.middleware_onion.add(local_filter_middleware)
    addr = MetaData().get_layer2_contract('ClearingHouse')
    abi  = AbiFactory().get_contract_abi('ClearingHouse')

    block_number: int = w3.eth.getBlock('latest').number
    contract = w3.eth.contract(address=addr, abi=abi)
    filter = contract.events.PositionChanged.createFilter(
        fromBlock=block_number-block_limit,
        toBlock=block_number
    )

    amm_pair_map = dict()

    for event in filter.get_all_entries():
        event_block_number = event.blockNumber
        event_block_timestamp = w3.eth.get_block(event_block_number).timestamp
        event_datetime = dt.datetime.fromtimestamp(event_block_timestamp).strftime("%Y/%m/%d %H:%M")
        tx_hash = event.transactionHash.hex()
        trader = event.args.trader
        value = event.args.positionNotional / ETH_DECIMALS
        pos_size = event.args.exchangedPositionSize / ETH_DECIMALS
        price = value / pos_size
        side = "buy" if pos_size > 0 else "sell"

        amm_addr = event.args.amm
        amm_abi  = AbiFactory().get_contract_abi('Amm')
        amm_contract = w3.eth.contract(address=amm_addr, abi=amm_abi)
        pair_name = amm_contract.functions.priceFeedKey().call().decode('utf-8').replace('\x00', '')

        print(tx_hash, pair_name, event_datetime)
        print(trader, value, pos_size, price, side)
        return event


def get_portfolio(trader: str):
    pass


def get_amm_info(amm_addr: str, amm_pair: str, short_name: bool = False):
    pass


def verify_function_data(contract_addr: str, byte_code: str):
    pass
