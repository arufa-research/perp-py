# PerpPy

| Build  | Coverage | PyPi | 
| ------------- | ------------- | ------------- |
| [![Tests](https://github.com/arufa-research/perp-py/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/arufa-research/perp-py/actions/workflows/python-package.yml) | ![Documentation Status(https://readthedocs.org/projects/perp-py/badge/?version=latest)](https://perp-py.readthedocs.io/en/latest/)  | [![PyPI version](https://badge.fury.io/py/perp-py.svg)](https://badge.fury.io/py/perp-py) |

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

## import query connector
from perppy.query import QueryConnector

## import execute connector
from perppy.execute import ExecuteConnector
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

### Running tests

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
from perppy.query import QueryConnector

query_conn = QueryConnector()

print(query_conn.get_position_changes())
print(query_conn.get_position_changes(pair='BTC/USDC'))
print(query_conn.get_position_changes(pair='BTC/USDC', block_limit=10))
```

+   Query trader portfolio using trader address. 

```python
from perppy.query import QueryConnector

query_conn = QueryConnector()

trader_portfolio = query_conn.get_trader_portfolio('')

print(trader_portfolio.layer1_balance)
print(trader_portfolio.layer2_balance)

print(trader_portfolio.portfolios['PERP/USDC'])
```

+   Query information of all AMMs or one AMM. `get_all_amms()` returns list of `Amm` objects. `get_amm_info(pair_name)` returns the `Amm` object for given `pair_name`.

```python
from perppy.query import QueryConnector

query_conn = QueryConnector()

amm_list = query_conn.get_all_amms()

btc_amm = query_conn.get_amm_info('BTC/USDC')
print(btc_amm.addr)
print(btc_amm.market_price)
```

### Execute transactions

### Staking

### Faucet

## Documentation

Quickstart and API reference documentation is on [ReadTheDocs](https://perp-py.readthedocs.io/en/latest/).
