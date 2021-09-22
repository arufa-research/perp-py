

class Portfolio:
    def __init__(self):
        self.trader_addr  = None
        self.amm_addr     = None
        self.pair_name    = None

        self.pos_size     = None
        self.margin       = None
        self.margin_ratio = None
        self.leverage     = None
        self.pnl          = None
        self.liq_price    = None
        self.notional_val = None
        self.last_block   = None

    def __repr__(self):
        retStr = f"Portfolio("
        retStr += f"Trader address: {self.trader_addr}, "
        retStr += f"AMM address: {self.amm_addr}, "
        retStr += f"Pair: {self.pair_name}, "
        retStr += f"Position Size: {self.pos_size}, "
        retStr += f"Margin (with funding payment): {self.margin}, "
        retStr += f"Margin ratio: {self.margin_ratio}, "
        retStr += f"Leverage: {self.leverage}, "
        retStr += f"PnL: {self.pnl}, "
        retStr += f"Liquidation price: {self.liq_price}, "
        retStr += f"Open notional: {self.notional_val}, "
        retStr += f"Last open at block: {self.last_block})"
        return retStr
