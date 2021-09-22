


class Trader:
    def __init__(self, layer1_balance, layer2_balance, portfolios):
        self.addr           = None
        self.layer1_balance = layer1_balance
        self.layer2_balance = layer2_balance

        self.portfolios = dict()    # pair_name: Portfolio
        self._store_portfolios(portfolios)

    def _store_portfolios(self, portfolios):
        for portfolio in portfolios:
            self.portfolios[portfolio.pair_name] = portfolio

    def __repr__(self):
        retStr = f"Trader("
        retStr += f"Address: {self.addr}, "
        retStr += f"Layer 1 balance: {self.layer1_balance}, "
        retStr += f"Layer 2 balance: {self.layer2_balance}, "
        retStr += f"Portfolios: {list(self.portfolios.values())})"
        return retStr
