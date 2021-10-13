


class Trader:
    """
    Trader object stores the information of a given trader.

    Trader object is returned when trader information
    is queried from contracts.
    """
    def __init__(self, layer1_balance, layer2_balance, portfolios):
        """
        Create a new Trader object.

        :param layer1_balance: Layer1 USDC balance of trader
        :param layer2_balance: Layer1 USDC balance of trader
        :param portfolios: list of `Portfolio` objects, each for an AMM pair with non-zero balance
        """
        self.addr           = None
        self.layer1_balance = layer1_balance
        self.layer2_balance = layer2_balance

        self.portfolios = dict()    # pair_name: Portfolio
        self._store_portfolios(portfolios)

    def _store_portfolios(self, portfolios):
        """
        Stores the portfolios in the object as a dictionary.
        Used internally by the class constructor.

        :param portfolios: list of `Portfolio` objects, each for an AMM pair with non-zero balance
        """
        for portfolio in portfolios:
            self.portfolios[portfolio.pair_name] = portfolio

    def __repr__(self):
        """
        String representation of Trader object. 
        """
        retStr = f"Trader("
        retStr += f"Address: {self.addr}, "
        retStr += f"Layer 1 balance: {self.layer1_balance}, "
        retStr += f"Layer 2 balance: {self.layer2_balance}, "
        retStr += f"Portfolios: {list(self.portfolios.values())})"
        return retStr
