class Account():
    def __init__(self, client):
        """
        Initialize the Account client with a reference to the main API client.

        Args:
            client: The main API client instance.
        """
        self.client = client

    def balance(self):
        """
        Get the wallet balance for the organization this API key belongs to,
        along with the minutes it buys, the active plan, concurrency headroom,
        and auto-recharge settings.

        Reads the caller's own organization. There is no parameter for reading
        another account; resellers use the reseller endpoints for a client's
        figures.

        The API key's user needs Billing access in the organization, or the
        request fails with 403.

        `balance["can_place_calls"]` covers credit only. An account stopped
        for any other reason never reaches this endpoint; every request
        returns 403. `estimated_minutes_remaining` is an estimate at today's
        rates, `None` where a rate is not set, and 0 when the balance buys
        nothing (including when it is negative).

        Returns:
            dict: Response containing the account balance details.

        Example:
            wallet = client.account.balance()["json"]
            if not wallet["balance"]["can_place_calls"]:
                raise SystemExit("Out of credit. Top up before dialing.")
        """
        return self.client.get("account/balance")
