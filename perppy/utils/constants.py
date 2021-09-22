
ETH_DECIMALS = 10**18

MAINTENANCE_MARGIN_RATIO = 0.0625 * ETH_DECIMALS

PRODUCTION_METADATA_URL = "https://metadata.perp.exchange/production.json"
STAGING_METADATA_URL    = "https://metadata.perp.exchange/staging.json"

INFURA_PROJECT_ID = "04034d1ba6d141b4a5d57f872c0e52bd"  # read from env instead
xDAI_URL          = "https://rpc.xdaichain.com/"
RINKEBY_URL       = "https://rinkeby.infura.io/v3/" + INFURA_PROJECT_ID
HOMESTEAD_URL     = "https://mainnet.infura.io/v3/" + INFURA_PROJECT_ID

NETWORK_NAMES = ["xDai", "Rinkeby", "Homestead"]
LAYER_MAP = {
    "layer1": {
        "production": "Homestead",
        "staging": "Rinkeby",
    },
    "layer2": {
        "production": "xDai",
        "staging": "xDai",
    }
}

NETWORK_MAP = {
    "xDai": xDAI_URL,
    "Rinkeby": RINKEBY_URL,
    "Homestead": HOMESTEAD_URL,
}


def get_network_url(network_name: str) -> str:
    if network_name not in NETWORK_MAP:
        raise ValueError(f"Invalid network name {network_name}, available: {list(NETWORK_MAP.keys())}")
    return NETWORK_MAP[network_name]
