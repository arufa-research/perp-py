from web3 import Web3
from web3.middleware import local_filter_middleware

from perppy.utils.singleton import Singleton
from perppy.utils.constants import get_network_url, NETWORK_MAP


class Web3ProviderFactory(metaclass=Singleton):
    def __init__(self):
        self.provider_map = dict()
        for name, url in NETWORK_MAP.items():
            w3_provider = Web3(Web3.HTTPProvider(url))
            w3_provider.middleware_onion.add(local_filter_middleware)

            self.provider_map[name] = w3_provider

    def get_provider(self, name=None):
        if name in self.provider_map:
            return self.provider_map[name]
        else:
            raise ValueError(f"Invalid network name {name}")
