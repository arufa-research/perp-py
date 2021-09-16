import json
import requests

from perppy.utils.singleton import Singleton
from perppy.utils.constants import PRODUCTION_METADATA_URL, STAGING_METADATA_URL


class MetaData(metaclass=Singleton):
    def __init__(self):
        self.production_metadata = None
        self.staging_metadata    = None

        self._fetch_production_metadata()
        self._fetch_staging_metadata()

    def _fetch_production_metadata(self):
        self.production_metadata = requests.get(PRODUCTION_METADATA_URL).json()

    def _fetch_staging_metadata(self):
        self.staging_metadata = requests.get(STAGING_METADATA_URL).json()

    def get_layer1_contract(self, contract_name: str, network: str = "production"):
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
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer1"]["contracts"]

    def get_layer1_name(self, network: str = "production"):
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer1"]["network"]

    def get_layer1_external_contracts(self, network: str = "production"):
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer1"]["externalContracts"]

    def get_layer2_contract(self, contract_name: str, network: str = "production"):
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
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer2"]["contracts"]

    def get_layer2_name(self, network: str = "production"):
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer2"]["network"]

    def get_layer2_external_contracts(self, network: str = "production"):
        if network not in ["production", "staging"]:
            raise ValueError(f"Invalid network type {network}, should be either production or staging")

        metadata = self.production_metadata if network == "production" else self.staging_metadata
        return metadata["layers"]["layer2"]["externalContracts"]
