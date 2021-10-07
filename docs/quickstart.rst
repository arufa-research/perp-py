Quickstart
==========

.. contents:: :local:

.. NOTE:: All code starting with a ``$`` is meant to run on your terminal.

Installation
------------

Perp-py can be installed using ``pip`` as follows:

.. code-block:: shell

   $ pip install perp-py


Using perp-py
-------------

This library depends on a connection to an Ethereum node for layer1 contracts and xDai node for layer2 contracts. The connections to the Perpetual cotracts (on either staging or production nodes) are made using Connector objects which are ``QueryConnector``, ``ExecuteConnector`` and ``StakingConnector``. 

The data or responnse received on querying data or executing a transaction is wrapped into msg objects which comes with built-in useful methods, a few which are shown below. 

This Quickstart guide will highlight few of the most common use cases.


Query data from contracts
*************************

Query recent positions. User can specify the network (production/staging) and add filters such as trader address, block limit and pair name. ``get_position_changes()`` returns a list of ``Position`` objects. 

.. code-block:: python

    from perppy.query import QueryConnector

    query_conn = QueryConnector(network='production')

    print(query_conn.get_position_changes())
    print(query_conn.get_position_changes(pair='BTC/USDC'))
    print(query_conn.get_position_changes(pair='BTC/USDC', block_limit=10))


Query trader portfolio using trader address. 

.. code-block:: python

    from perppy.query import QueryConnector

    query_conn = QueryConnector(network='production')

    trader_portfolio = query_conn.get_trader_portfolio('')

    print(trader_portfolio.layer1_balance)
    print(trader_portfolio.layer2_balance)

    print(trader_portfolio.portfolios['PERP/USDC'])


Query information of all AMMs or one AMM. ``get_all_amms()`` returns list of ``Amm`` objects. ``get_amm_info(pair_name)`` returns the ``Amm`` object for given ``pair_name``.

.. code-block:: python

    from perppy.query import QueryConnector

    query_conn = QueryConnector(network='production')

    amm_list = query_conn.get_all_amms()

    btc_amm = query_conn.get_amm_info('BTC/USDC')
    print(btc_amm.addr)
    print(btc_amm.market_price)


Execute trades, update positions
********************************

Export environment variable for your account's private key:

.. code-block:: bash

    $ export PRIVATE_KEY='<YOUR_KEY_HERE>'


.. NOTE:: Above variable exported is ``PRIVATE_KEY``, so first argument in constructor of ``ExecuteConnector`` should be ``'PRIVATE_KEY'``.

Deposit USDC to layer 2 (xDai).

.. code-block:: python

    from perppy.execute import ExecuteConnector

    exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
    response = exec_conn.deposit_to_layer2(1000)   # 1000.0 USDC
    print(response)


Withdraw USDC from layer 2 (xDai).

.. code-block:: python

    from perppy.execute import ExecuteConnector

    exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
    response = exec_conn.withdraw_from_layer2(1000)   # 1000.0 USDC
    print(response)


Open position.

.. code-block:: python

    from perppy.execute import ExecuteConnector

    exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
    response = exec_conn.open_position(1000)   # 1000.0 USDC
    print(response)


Close position.

.. code-block:: python

    from perppy.execute import ExecuteConnector

    exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
    response = exec_conn.close_position(1000)   # 1000.0 USDC
    print(response)


Add margin.

.. code-block:: python

    from perppy.execute import ExecuteConnector

    exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
    response = exec_conn.add_margin(1000)   # 1000.0 USDC
    print(response)


Remove margin.

.. code-block:: python

    from perppy.execute import ExecuteConnector

    exec_conn = ExecuteConnector('PRIVATE_KEY', network='staging')
    response = exec_conn.remove_margin(1000)   # 1000.0 USDC
    print(response)


Staking
*****************


