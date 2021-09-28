# PerpPy

Python SDK for Perpetual Protocol.

## Installation

```bash
$ pip install perp-py
```

## Installing from source

### Running locally without installation

```bash
$ git clone https://github.com/arufa-research/perp-py
$ cd perp-py/

$ python3
```

In python interpreter:

```python
# import the whole library
import perpy

## import query functions
from perppy.query import *

## import execute functions
from perppy.execute import *
```

### Installation

```bash
$ git clone https://github.com/arufa-research/perp-py
$ cd perp-py/
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ make install
```

### Testing

```bash
$ git clone https://github.com/arufa-research/perp-py
$ cd perp-py/
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ make test
```

## Example Usage

### Query data

+   Query recent positions. User can specify the network (production/staging) and add filters such as trader address, block limit and pair name. `get_position_changes()` returns a list of `Position` objects. 

```python
from perppy.query import get_position_changes

print(get_position_changes())
print(get_position_changes(pair='BTC/USDC'))
print(get_position_changes(pair='BTC/USDC', block_limit=10))
print(get_position_changes(network='staging'))
```

+   Query trader portfolio using trader address. 

```python
from perppy.query import get_trader_portfolio

trader_portfolio = get_trader_portfolio('')

print(trader_portfolio.layer1_balance)
print(trader_portfolio.layer2_balance)

print(trader_portfolio.portfolios['PERP/USDC'])
```

+   Query information of all AMMs or one AMM. `get_all_amms()` returns list of `Amm` objects. `get_amm_info(pair_name)` returns the `Amm` object for given `pai_name`.

```python
from perppy.query import get_all_amms, get_amm_info

amm_list = get_all_amms()

btc_amm = get_amm_info('BTC/USDC')
print(btc_amm.addr)
print(btc_amm.market_price)
```

### Execute transactions

### Staking

### Faucet

## Documentation

Quickstart and API reference documentation is on [ReadTheDocs]().
