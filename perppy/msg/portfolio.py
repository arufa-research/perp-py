
from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.utils.constants import ETH_DECIMALS, MAINTENANCE_MARGIN_RATIO
from perppy.utils.provider import Web3ProviderFactory


class Portfolio:
    """
    Portfolio object stores the portfolio related information of a given trader for a given AMM pair.

    This class contains all the information related to the position
    a trader has for a given AMM pair.

    Portfolio object is returned portfolio or balances related information
    is queried from contracts.
    """
    def __init__(self, amm_addr, trader_addr, network):
        """
        Create a new Portfolio object.

        :param amm_addr: Address of Amm pair
        :param trader_addr: Address of trader
        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        self.amm_addr     = amm_addr
        self.trader_addr  = trader_addr
        self.pair_name    = None

        self.pos_size     = None
        self.margin       = None
        self.margin_ratio = None
        self.leverage     = None
        self.pnl          = None
        self.liq_price    = None
        self.notional_val = None
        self.last_block   = None

        self._fetch_values(network)

    def _fetch_values(self, network):
        """
        Fetches information of position of a trader `self.trader_addr` for Amm with address `self.amm_addr` from input network.
        Used internally by the class constructor.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        w3_provider = Web3ProviderFactory().get_layer2_provider(network)
        clearing_house_viewer_addr = MetaData().get_layer2_contract('ClearingHouseViewer')
        clearing_house_viewer_abi  = AbiFactory().get_contract_abi('ClearingHouseViewer')
        clearing_house_viewer_contract = w3_provider.eth.contract(address=clearing_house_viewer_addr, abi=clearing_house_viewer_abi)

        clearing_house_addr = MetaData().get_layer2_contract('ClearingHouse')
        clearing_house_abi  = AbiFactory().get_contract_abi('ClearingHouse')
        clearing_house_contract = w3_provider.eth.contract(address=clearing_house_addr, abi=clearing_house_abi)

        amm_pos = clearing_house_viewer_contract.functions.getPersonalPositionWithFundingPayment(self.amm_addr, self.trader_addr).call()
        if amm_pos[0][0] == 0:  # position size is 0
            return None
        self.pos_size     = amm_pos[0][0] / ETH_DECIMALS
        self.margin       = amm_pos[1][0] / ETH_DECIMALS
        self.notional_val = amm_pos[2][0] / ETH_DECIMALS
        self.last_block   = amm_pos[5]

        amm_abi  = AbiFactory().get_contract_abi('Amm')
        amm_contract = w3_provider.eth.contract(address=self.amm_addr, abi=amm_abi)
        self.pair_name = amm_contract.functions.priceFeedKey().call().decode('utf-8').replace('\x00', '') + "/USDC"

        amm_margin_ratio = clearing_house_viewer_contract.functions.getMarginRatio(self.amm_addr, self.trader_addr).call()
        self.margin_ratio = amm_margin_ratio[0]

        pos_notional_and_pnl = clearing_house_contract.functions.getPositionNotionalAndUnrealizedPnl(
            self.amm_addr,
            self.trader_addr,
            0
        ).call()
        self.pnl = pos_notional_and_pnl[1][0] / ETH_DECIMALS
        self.leverage = pos_notional_and_pnl[0][0] / (amm_pos[1][0] + pos_notional_and_pnl[1][0])

        # self.liq_price = 

    def __repr__(self):
        """
        String representation of Portfolio object.
        """
        retStr = f"Portfolio("
        retStr += f"Trader address: {self.trader_addr}, "
        retStr += f"AMM address: {self.amm_addr}, "
        retStr += f"Pair: {self.pair_name}, "
        retStr += f"Position Size: {self.pos_size}, "
        retStr += f"Margin (with funding payment): {self.margin}, "
        retStr += f"Margin ratio: {self.margin_ratio}, "
        retStr += f"Leverage: {self.leverage}, "
        retStr += f"PnL: {self.pnl}, "
        retStr += f"Liquidation price: {self.liq_price}, "
        retStr += f"Open notional: {self.notional_val}, "
        retStr += f"Last open at block: {self.last_block})"
        return retStr
