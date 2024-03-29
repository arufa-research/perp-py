# PerpPy

| Build  | Docs | PyPi | 
| ------------- | ------------- | ------------- |
| [![Tests](https://github.com/arufa-research/perp-py/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/arufa-research/perp-py/actions/workflows/build.yml) | [![Docs](https://readthedocs.org/projects/perp-py/badge/?version=latest)](https://perp-py.readthedocs.io/en/latest/)  | [![PyPI version](https://badge.fury.io/py/perp-py.svg)](https://badge.fury.io/py/perp-py) |

Python SDK for Perpetual Protocol.

## Installation

```bash
$ pip install perp-py
```

## Installation from source

```bash
$ git clone https://github.com/arufa-research/perp-py
$ cd perp-py/
$ python3 -m venv env
$ source env/bin/activate
$ make install
```

### Run tests

```bash
$ make test
```

### Run linter

```bash
$ make lint
```

### Generate docs

```bash
$ make docs
```

## Run locally without installation

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

## Example Usage

### Query data

+   Query recent positions. User can specify the network (production/staging) and add filters such as trader address, block limit and pair name. `get_position_changes()` returns a list of `Position` objects. 

```python
from perppy.query import QueryConnector

query_conn = QueryConnector(network='production')

print(query_conn.get_position_changes())
print(query_conn.get_position_changes(pair='BTC/USDC'))
print(query_conn.get_position_changes(pair='BTC/USDC', block_limit=10))
```

+   Query trader portfolio using trader address. 

```python
from perppy.query import QueryConnector

query_conn = QueryConnector(network='production')

trader_portfolio = query_conn.get_trader_portfolio('')

print(trader_portfolio.layer1_balance)
print(trader_portfolio.layer2_balance)

print(trader_portfolio.portfolios['PERP/USDC'])
```

+   Query information of all AMMs or one AMM. `get_all_amms()` returns list of `Amm` objects. `get_amm_info(pair_name)` returns the `Amm` object for given `pair_name`.

```python
from perppy.query import QueryConnector

query_conn = QueryConnector(network='production')

amm_list = query_conn.get_all_amms()

btc_amm = query_conn.get_amm_info('BTC/USDC')
print(btc_amm.addr)
print(btc_amm.market_price)
```

### Execute transactions

Export environment variable for your account's private key:

```bash
$ export PRIVATE_KEY='<YOUR_KEY_HERE>'
```

**Note**: Above variable exported is `PRIVATE_KEY`, so first argument in constructor of `ExecuteConnector` should be `'PRIVATE_KEY'`.

+   Deposit USDC to layer 2 (xDai).

```python
from perppy.execute import ExecuteConnector

exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
response = exec_conn.deposit_to_layer2(1000)   # 1000.0 USDC
print(response)
```

+   Withdraw USDC from layer 2 (xDai).

```python
from perppy.execute import ExecuteConnector

exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
response = exec_conn.withdraw_from_layer2(1000)   # 1000.0 USDC
print(response)
```

+   Open position.

```python
from perppy.execute import ExecuteConnector

exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
response = exec_conn.open_position(1000)   # 1000.0 USDC
print(response)
```

+   Close position.

```python
from perppy.execute import ExecuteConnector

exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
response = exec_conn.close_position(1000)   # 1000.0 USDC
print(response)
```

+   Add margin.

```python
from perppy.execute import ExecuteConnector

exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
response = exec_conn.add_margin(10)
print(response)
```

+   Remove margin.

```python
from perppy.execute import ExecuteConnector

exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
response = exec_conn.remove_margin(10)
print(response)
```

### Staking

Export environment variable for your account's private key:

```bash
$ export PRIVATE_KEY='<YOUR_KEY_HERE>'
```

**Note**: Above variable exported is `PRIVATE_KEY`, so first argument in constructor of `StakingConnector` should be `'PRIVATE_KEY'`.

+ Get PERP staking info.

```python
from perppy.staking import StakingConnector

staking_conn = StakingConnector(network='staging') # no need to private key for fetching info
stats = staking_conn.get_current_stats()
print(stats)
```


## Documentation

Quickstart and API reference documentation is on [ReadTheDocs](https://perp-py.readthedocs.io/en/latest/).
