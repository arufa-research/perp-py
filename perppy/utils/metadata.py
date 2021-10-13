import json
import requests

from perppy.utils.singleton import Singleton
from perppy.utils.constants import PRODUCTION_METADATA_URL, STAGING_METADATA_URL


class MetaData(metaclass=Singleton):
    """
    Metadata singleton class is used to fetch and store metdata information
    such as RPC url, contract addresses. 
    """
    def __init__(self):
        """
        Initiates the MetaData singleton class and fetches raw data from `perp.exchange`. This method is called
        when user first calls any of the other Metadata() methods.
        """
        self.production_metadata = None
        self.staging_metadata    = None

        self._fetch_production_metadata()
        self._fetch_staging_metadata()

    def _fetch_production_metadata(self):
        """
        Fetches the production metadata as raw JSON.
        """
        self.production_metadata = requests.get(PRODUCTION_METADATA_URL).json()

    def _fetch_staging_metadata(self):
        """
        Fetches the staging metadata as raw JSON.
        """
        self.staging_metadata = requests.get(STAGING_METADATA_URL).json()

    def get_layer1_contract(self, contract_name: str, network: str = "production"):
        """
        Get layer1 contract address with name `contract_name`
        and on network `network`.

        :param contract_name: Name of contract
        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        contracts = metadata["layers"]["layer1"]["contracts"]
        external_contracts = metadata["layers"]["layer1"]["externalContracts"]
        if contract_name in contracts:
            return contracts[contract_name]["address"]
        elif contract_name in external_contracts:
            return external_contracts[contract_name]
        else:
            raise ValueError(
                f"Invalid contract name {contract_name}, avaliable contracts {list(contracts.keys())+list(external_contracts.keys())}"
            )

    def get_layer1_contracts(self, network: str = "production"):
        """
        Get list of layer1 contracts on network `network`.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer1"]["contracts"]

    def get_layer1_name(self, network: str = "production"):
        """
        Get layer1 network name.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer1"]["network"]

    def get_layer1_external_contracts(self, network: str = "production"):
        """
        Get list of layer1 external contracts on network `network`.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer1"]["externalContracts"]

    def get_layer2_contract(self, contract_name: str, network: str = "production"):
        """
        Get layer2 contract address with name `contract_name`
        and on network `network`.

        :param contract_name: Name of contract
        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        contracts = metadata["layers"]["layer2"]["contracts"]
        external_contracts = metadata["layers"]["layer2"]["externalContracts"]
        if contract_name in contracts:
            return contracts[contract_name]["address"]
        elif contract_name in external_contracts:
            return external_contracts[contract_name]
        else:
            raise ValueError(
                f"Invalid contract name {contract_name}, avaliable contracts {list(contracts.keys())+list(external_contracts.keys())}"
            )

    def get_layer2_contracts(self, network: str = "production"):
        """
        Get list of layer2 contracts on network `network`.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer2"]["contracts"]

    def get_layer2_name(self, network: str = "production"):
        """
        Get layer2 network name.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer2"]["network"]

    def get_layer2_external_contracts(self, network: str = "production"):
        """
        Get list of layer2 external contracts on network `network`.

        :param network: Network to connect to. Valid values are 'production' and 'staging'
        """
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer2"]["externalContracts"]
