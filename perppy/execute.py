# import time
from enum import IntEnum
from web3 import Web3

from perppy.msg.amm import Amm
# from perppy.msg.trader import Trader
from perppy.utils.abi import AbiFactory
from perppy.utils.metadata import MetaData
# from perppy.msg.portfolio import Portfolio
from perppy.utils.provider import Web3ProviderFactory
# from perppy.msg.event.position_changed import PositionChanged
from perppy.utils.constants import get_network_url, ETH_DECIMALS, DEFAULT_LAYER1_GAS_PRICE, DEFAULT_LAYER2_GAS_PRICE


class Side(IntEnum):
    LONG  = 0
    SHORT = 1


class ExecuteConnector:
    def __init__(self, mnemonic: str, network = 'production'):
        self.network         = network
        self.layer1_provider = Web3ProviderFactory().get_layer1_provider(self.network)
        self.layer2_provider = Web3ProviderFactory().get_layer2_provider(self.network)

        self.layer1_account  = self.layer1_provider.eth.account.privateKeyToAccount(mnemonic)
        self.layer2_account  = self.layer2_provider.eth.account.privateKeyToAccount(mnemonic)

    def _approve_layer1_bridge( # bridge from layer 1 to layer 2
        self,
        usdc_amount,
    ):
        layer1_bridge_addr = Web3.toChecksumAddress(MetaData().get_layer1_contract('RootBridge', network=self.network))

        layer1_usdc_addr = Web3.toChecksumAddress('0x40d3b2f06f198d2b789b823cdbecd1db78090d74')
        layer1_usdc_abi  = AbiFactory().get_contract_abi('usdc')
        layer1_usdc_contract = self.layer1_provider.eth.contract(address=layer1_usdc_addr, abi=layer1_usdc_abi)

        nonce = self.layer1_provider.eth.get_transaction_count(self.layer1_account.address)
        approve_transaction = layer1_usdc_contract.functions.approve(layer1_bridge_addr, usdc_amount*ETH_DECIMALS).buildTransaction({
            'nonce': nonce,
            'gas': 1000000,
            'gasPrice': self.layer1_provider.eth.gasPrice,
        })
        signed_tx = self.layer1_provider.eth.account.sign_transaction(approve_transaction, private_key=self.layer1_account.key)
        
        tx_hash = self.layer1_provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.layer1_provider.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def _approve_layer2_bridge( # bridge from layer 2 to layer 1
        self,
        usdc_amount,
    ):
        pass

    def deposit_to_layer2(
        self,
        usdc_amount: float,
    ):
        if usdc_amount <= 0.0:
            raise ValueError(f"Invalid USDC amount, {usdc_amount}")

        # approve bridge to use usdc
        receipt = self._approve_layer1_bridge(usdc_amount)

        # deposit usdc and return receipt
        layer1_bridge_addr = Web3.toChecksumAddress(MetaData().get_layer1_contract('RootBridge', network=self.network))
        layer1_bridge_abi  = AbiFactory().get_contract_abi('RootBridge')
        layer1_bridge_contract = self.layer1_provider.eth.contract(address=layer1_bridge_addr, abi=layer1_bridge_abi)

        layer1_usdc_addr = Web3.toChecksumAddress(MetaData().get_layer1_contract('usdc', network=self.network))
        layer1_usdc_abi  = AbiFactory().get_contract_abi('usdc')
        layer1_usdc_contract = self.layer1_provider.eth.contract(address=layer1_usdc_addr, abi=layer1_usdc_abi)

        nonce = self.layer1_provider.eth.get_transaction_count(self.layer1_account.address)
        transfer_transaction = layer1_bridge_contract.functions.erc20Transfer(layer1_usdc_addr, self.layer1_account.address, {'d':usdc_amount*ETH_DECIMALS}).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice': self.layer1_provider.eth.gasPrice,
        })
        signed_tx = self.layer1_provider.eth.account.sign_transaction(transfer_transaction, private_key=self.layer1_account.key)
        tx_hash = self.layer1_provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.layer1_provider.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def withdraw_from_layer2(
        self,
        usdc_amount: float,
    ):
        if usdc_amount <= 0.0:
            raise ValueError(f"Invalid USDC amount, {usdc_amount}")

        # approve bridge to use usdc
        self._approve_layer2_bridge(usdc_amount)

        # withdraw usdc and return receipt

    def open_position(
        self,
        amm_addr: str,
        side: int,
        quote_asset_amount: float,
        leverage: int,
        base_asset_amount_limit: float,
        gasLimit: float = 0.,
    ):
        if side not in [Side.LONG, Side.SHORT]:
            raise ValueError(f"Invalid side, {side}")

        if quote_asset_amount <= 0.0:
            raise ValueError(f"Invalid Quote asset amount, {quote_asset_amount}")

        if leverage <= 0 or leverage > 10:
            raise ValueError(f"Invalid leverage value, {leverage}")

        # clearing_house_viewer_addr = MetaData().get_layer2_contract('ClearingHouseViewer', network=self.network)
        # clearing_house_viewer_abi  = AbiFactory().get_contract_abi('ClearingHouseViewer')
        # clearing_house_viewer_contract = self.layer2_provider.eth.contract(address=clearing_house_viewer_addr, abi=clearing_house_viewer_abi)

        clearing_house_addr = MetaData().get_layer2_contract('ClearingHouse', network=self.network)
        clearing_house_abi  = AbiFactory().get_contract_abi('ClearingHouse')
        clearing_house_contract = self.layer2_provider.eth.contract(address=clearing_house_addr, abi=clearing_house_abi)

        nonce = self.layer2_provider.eth.get_transaction_count(self.layer2_account.address)
        transaction = clearing_house_contract.functions.openPosition(amm_addr, side, {'d': quote_asset_amount*ETH_DECIMALS}, {'d':leverage}, {'d':base_asset_amount_limit*ETH_DECIMALS}).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice':self.layer2_provider.eth.gasPrice
        })
        signed_tx = self.layer2_provider.eth.account.sign_transaction(transaction,private_key=self.layer2_account.key)
        tx_hash = self.layer2_provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.layer2_provider.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def close_position(
        self,
        amm_name: str,
        quote_asset_amount_limit: float,
    ):
        pass

    def add_margin(
        self,
        amm_name: str,
        margin: float,
    ):
        pass

    def remove_margin(
        self,
        amm_name: str,
        margin: float,
    ):
        pass
