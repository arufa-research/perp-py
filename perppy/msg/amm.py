
from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
from perppy.utils.provider import Web3ProviderFactory
from perppy.utils.constants import ETH_DECIMALS


class Amm:
    def __init__(self, amm_addr, network):
        self.addr      = amm_addr
        self.pair_name = None

        self.index_price = None
        self.market_price = None
        self.open_interest_notional_cap = None
        self.open_interest_notional = None
        self.max_holding_base_asset = None
        self.feed_name = None
        self.quote_asset_reserve = None
        self.base_asset_reserve = None

        self._fetch_data(network)

    def _fetch_data(self, network):
        w3_provider_layer2 = Web3ProviderFactory().get_layer2_provider(network)

        amm_abi  = AbiFactory().get_contract_abi('Amm')
        amm_contract = w3_provider_layer2.eth.contract(address=self.addr, abi=amm_abi)
        self.pair_name = amm_contract.functions.priceFeedKey().call().decode('utf-8').replace('\x00', '') + "/USDC"

        clearing_house_addr = MetaData().get_layer2_contract('ClearingHouse')
        clearing_house_abi  = AbiFactory().get_contract_abi('ClearingHouse')
        clearing_house_contract = w3_provider_layer2.eth.contract(address=clearing_house_addr, abi=clearing_house_abi)

        self.index_price = amm_contract.functions.getUnderlyingPrice().call()[0] / ETH_DECIMALS
        self.market_price = amm_contract.functions.getSpotPrice().call()[0] / ETH_DECIMALS
        self.open_interest_notional_cap = amm_contract.functions.getOpenInterestNotionalCap().call()[0] / ETH_DECIMALS
        self.max_holding_base_asset = amm_contract.functions.getMaxHoldingBaseAsset().call()[0] / ETH_DECIMALS

        reserve = amm_contract.functions.getReserve().call()
        self.quote_asset_reserve = reserve[0][0] / ETH_DECIMALS
        self.base_asset_reserve = reserve[1][0] / ETH_DECIMALS
        self.open_interest_notional = clearing_house_contract.functions.openInterestNotionalMap(self.addr).call() / ETH_DECIMALS

        price_feed = amm_contract.functions.priceFeed().call()
        if price_feed == MetaData().get_layer2_contract('L2PriceFeed'):
            self.feed_name = "L2PriceFeed"
        elif price_feed == MetaData().get_layer2_contract('ChainlinkPriceFeed'):
            self.feed_name = "ChainlinkPriceFeed"
        else:
            self.feed_name = None

    def __repr__(self):
        retStr = f"Amm("
        retStr += f"Address: {self.addr}, "
        retStr += f"Pair: {self.pair_name}, "
        retStr += f"Index price: {self.index_price} USDC, "
        retStr += f"Market price: {self.market_price} USDC, "
        retStr += f"OpenInterestNotionalCap: {self.open_interest_notional_cap} USDC, "
        retStr += f"OpenInterestNotional: {self.open_interest_notional} USDC, "
        retStr += f"MaxHoldingBaseAsset: {self.max_holding_base_asset}, "
        retStr += f"PriceFeed: {self.feed_name}, "
        retStr += f"QuoteAssetReserve: {self.quote_asset_reserve} USDC, "
        retStr += f"BaseAssetReserve: {self.base_asset_reserve})"
        return retStr
