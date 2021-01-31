class AccountInfo:
    """
    Default values are -1 for all
    """

    def __init__(self, customer_id: int = -1, premium_until: int = -1, limit_used: float = float(-1),
                 space_used: int = -1):
        self.customer_id = customer_id
        self.premium_until = premium_until
        self.limit_used = limit_used
        self.space_used = space_used



