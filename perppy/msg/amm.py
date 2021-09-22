

class Amm:
    def __init__(self):
        self.addr      = None
        self.pair_name = None

    def __repr__(self):
        retStr = f"Amm("
        retStr += f"Address: {self.addr}, "
        retStr += f"Pair: {self.pair_name}, "
        return retStr
