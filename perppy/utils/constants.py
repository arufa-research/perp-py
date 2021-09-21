

ETH_DECIMALS = 10**18

PRODUCTION_METADATA_URL = "https://metadata.perp.exchange/production.json"
STAGING_METADATA_URL    = "https://metadata.perp.exchange/staging.json"

INFURA_PROJECT_ID = "04034d1ba6d141b4a5d57f872c0e52bd"  # read from env instead
xDAI_URL          = "https://rpc.xdaichain.com/"
RINKEBY_URL       = "https://rinkeby.infura.io/v3/" + INFURA_PROJECT_ID
HOMESTEAD_URL     = "https://mainnet.infura.io/v3/" + INFURA_PROJECT_ID


def get_network_url(network_name: str) -> str:
    network_map = {
        "xDai": xDAI_URL,
        "Rinkeby": RINKEBY_URL,
        "Homestead": HOMESTEAD_URL,
    }
    if network_name not in network_map:
        raise ValueError(f"Invalid network name {network_name}, available: {list(network_map.keys())}")
    return network_map[network_name]
