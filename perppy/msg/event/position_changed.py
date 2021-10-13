import datetime as dt

from perppy.utils.abi import AbiFactory
from perppy.utils.provider import Web3ProviderFactory
from perppy.utils.constants import ETH_DECIMALS


class PositionChanged:
    """
    PositionChanged object stores the information of a position change event.

    PositionChanged object is returned when information related
    to changes in position is queried from contracts.
    """
    def __init__(self, event, network):
        """
        Create a new PositionChanged object.

        :param event: position changed event data fetched using web3.py
        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        self.tx_hash     = str()
        self.trader_addr = str()
        self.datetime    = None
        self.pair        = str()
        self.price       = float()
        self.value       = float()
        self.side        = str()
        self.pos_size    = float()

        self.network = network
        self._from_event(event)

    def _from_event(self, event):
        """
        Parses the information from event object and fetches additional info from input network.
        Used internally by the class constructor.

        :param event: position changed event data fetched using web3.py
        """
        w3_provider = Web3ProviderFactory().get_layer2_provider(self.network)
        event_block_number = event.blockNumber
        event_block_timestamp = w3_provider.eth.get_block(event_block_number).timestamp
        self.datetime = dt.datetime.fromtimestamp(event_block_timestamp).strftime("%Y/%m/%d %H:%M")
        self.tx_hash = event.transactionHash.hex()
        self.trader_addr = event.args.trader
        self.value = event.args.positionNotional / ETH_DECIMALS
        self.pos_size = event.args.exchangedPositionSize / ETH_DECIMALS
        self.price = self.value / self.pos_size
        self.side = "buy" if self.pos_size > 0 else "sell"

        amm_addr = event.args.amm
        amm_abi  = AbiFactory().get_contract_abi('Amm')
        amm_contract = w3_provider.eth.contract(address=amm_addr, abi=amm_abi)
        self.pair = amm_contract.functions.priceFeedKey().call().decode('utf-8').replace('\x00', '')

    def __repr__(self):
        """
        String representation of PositionChanged object. 
        """
        retStr = f"PositionChanged("
        retStr += f"estimated time: {self.datetime}, "
        retStr += f"trader: {self.trader_addr}, "
        retStr += f"asset: {self.pair}, "
        retStr += f"side: {self.side}, "
        retStr += f"price: {self.price}, "
        retStr += f"size: {self.pos_size}, "
        retStr += f"tx: {self.tx_hash})"
        return retStr
