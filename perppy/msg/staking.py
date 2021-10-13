


class StakingStats:
    """
    StakingStats object stores the information related to staking.

    StakingStats object is returned when staking related information
    is queried from contracts.
    """
    def __init__(self, seed_allocation, perp_balance, vesting_allowance, novesting_allowance):
        """
        Create a new StakingStats object.

        :param seed_allocation: Seed allocation value for last week
        :param perp_balance: Current balance of PERP on reward governance contract
        :param vesting_allowance: PERP staking reward vesting allowance
        :param novesting_allowance: PERP staking reward noVesting allowance
        """
        self.last_week_seed_allocation = seed_allocation
        self.next_week_seed_allocation = seed_allocation+1
        self.perp_balance              = perp_balance
        self.vesting_allowance         = vesting_allowance
        self.novesting_allowance       = novesting_allowance

    def __repr__(self):
        """
        String representation of StakingStats object. 
        """
        retStr = f"StakingStats("
        retStr += f"Last week number of seed allocation: {self.last_week_seed_allocation}, "
        retStr += f"Next week number of seed allocation: {self.next_week_seed_allocation}, "
        retStr += f"PERP balance of reward governance: {self.perp_balance}, "
        retStr += f"vesting allowance: {self.vesting_allowance}, "
        retStr += f"noVesting allowance: {self.novesting_allowance})"
        return retStr
