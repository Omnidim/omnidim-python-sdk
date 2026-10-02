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

        A balance at or below zero does not always mean calls will stop.
        Check `plan["is_usage_based"]` first: such an organization keeps
        placing calls and is metered to its payment method instead.

        `estimated_minutes_remaining` is an estimate at today's voice-AI rate,
        `None` where no rate is set, and 0 when the balance buys nothing
        (including when it is negative). It excludes telephony: phone calls
        also pay telephony out of the same balance, so for phone calls the
        real figure is lower.

        `auto_recharge["amount_usd"]` is headroom above the threshold, not a
        fixed top-up: a recharge restores the balance to
        `threshold_usd + amount_usd`.

        Returns:
            dict: Response containing the account balance details.

        Example:
            wallet = client.account.balance()["json"]
            print(wallet["balance"]["amount"], wallet["estimated_minutes_remaining"])
        """
        return self.client.get("account/balance")
