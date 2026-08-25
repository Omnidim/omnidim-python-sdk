class Reseller():
    def __init__(self, client):
        """
        Initialize the Reseller client with a reference to the main API client.

        Args:
            client: The main API client instance.
        """
        self.client = client

    def list_organizations(self):
        """
        List the child organizations under this reseller account.

        Returns:
            dict: Response containing the list of child organizations.
        """
        return self.client.get("reseller/organizations")

    def add_user(self, name, email, phone, password, welcome_minutes_to_credit=None,
                 cost_per_min=None, concurrent_call_limit=None, expiry_date=None,
                 user_currency=None):
        """
        Create a new child user under this reseller account.

        Args:
            name (str): Name of the new user.
            email (str): Email of the new user.
            phone (str): Phone number of the new user.
            password (str): Password for the new user.
            welcome_minutes_to_credit (int): Minutes to credit on account creation (optional).
            cost_per_min (float): Cost per minute to charge the new user (optional).
            concurrent_call_limit (int): Max concurrent calls for the new user (optional).
            expiry_date (str): Account expiry date (optional).
            user_currency (str): Currency for the new user's account (optional).

        Returns:
            dict: Response containing the created user details.

        Raises:
            ValueError: If name, email, phone, or password is not provided.
        """
        if not name:
            raise ValueError("name is required.")
        if not email:
            raise ValueError("email is required.")
        if not phone:
            raise ValueError("phone is required.")
        if not password:
            raise ValueError("password is required.")

        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'password': password
        }
        if welcome_minutes_to_credit is not None:
            data['welcome_minutes_to_credit'] = welcome_minutes_to_credit
        if cost_per_min is not None:
            data['cost_per_min'] = cost_per_min
        if concurrent_call_limit is not None:
            data['concurrent_call_limit'] = concurrent_call_limit
        if expiry_date is not None:
            data['expiry_date'] = expiry_date
        if user_currency is not None:
            data['user_currency'] = user_currency

        return self.client.post("reseller/users/add", data=data)

    def set_access_control(self, user_id, dashboard_menu_access):
        """
        Set which dashboard menus a child user can access.

        Args:
            user_id (int): ID of the child user.
            dashboard_menu_access (dict): Map of menu flag name to bool.

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If user_id or dashboard_menu_access is not provided.
        """
        if user_id is None:
            raise ValueError("user_id is required.")
        if not isinstance(dashboard_menu_access, dict):
            raise ValueError("dashboard_menu_access must be a dict.")

        data = {
            'user_id': user_id,
            'dashboard_menu_access': dashboard_menu_access
        }
        return self.client.post("reseller/users/access-control", data=data)

    def set_expiry(self, user_id, expiry_date=None):
        """
        Set or clear the account expiry date for a child user.

        Args:
            user_id (int): ID of the child user.
            expiry_date (str): New expiry date, or None to clear the expiry.

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If user_id is not provided.
        """
        if user_id is None:
            raise ValueError("user_id is required.")

        # expiry_date is always included: passing None clears the expiry.
        data = {
            'user_id': user_id,
            'expiry_date': expiry_date
        }
        return self.client.post("reseller/users/expiry", data=data)

    def set_concurrency(self, child_organization_id, new_limit):
        """
        Set the concurrent call limit for a child organization.

        Args:
            child_organization_id (int): ID of the child organization.
            new_limit (int): The absolute concurrency limit to set (not a delta),
                must be >= 0.

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If child_organization_id is not provided, or new_limit is negative.
        """
        if child_organization_id is None:
            raise ValueError("child_organization_id is required.")
        if not isinstance(new_limit, int) or new_limit < 0:
            raise ValueError("new_limit must be an integer >= 0.")

        data = {
            'child_organization_id': child_organization_id,
            'new_limit': new_limit
        }
        return self.client.post("reseller/concurrency", data=data)

    def calculate_credits(self, minutes, cost_per_min=None, is_revert=False,
                           child_organization_id=None):
        """
        Calculate the credit cost for a number of minutes.

        Args:
            minutes (float): Number of minutes to calculate credits for.
            cost_per_min (float): Cost per minute to use in the calculation (optional).
            is_revert (bool): Whether this is a revert calculation (default: False).
            child_organization_id (int): ID of the child organization the calculation
                applies to (optional).

        Returns:
            dict: Response containing the calculated credit amount.

        Raises:
            ValueError: If minutes is not provided.
        """
        if minutes is None:
            raise ValueError("minutes is required.")

        data = {
            'minutes': minutes,
            'is_revert': is_revert
        }
        if cost_per_min is not None:
            data['cost_per_min'] = cost_per_min
        if child_organization_id is not None:
            data['child_organization_id'] = child_organization_id

        return self.client.post("reseller/credits/calculate", data=data)

    def transfer_credits(self, to_organization_id, minutes, cost_per_min):
        """
        Transfer credits from this reseller account to a child organization.

        Args:
            to_organization_id (int): ID of the child organization to credit.
            minutes (float): Number of minutes to transfer.
            cost_per_min (float): Cost per minute used to price the transfer.

        Returns:
            dict: Response containing the new balances for both accounts.

        Raises:
            ValueError: If any argument is not provided.
        """
        if to_organization_id is None:
            raise ValueError("to_organization_id is required.")
        if minutes is None:
            raise ValueError("minutes is required.")
        if cost_per_min is None:
            raise ValueError("cost_per_min is required.")

        data = {
            'to_organization_id': to_organization_id,
            'minutes': minutes,
            'cost_per_min': cost_per_min
        }
        return self.client.post("reseller/credits/transfer", data=data)

    def revert_credits(self, from_organization_id, minutes):
        """
        Revert previously transferred credits from a child organization.

        Deliberately takes no rate: the revert uses the rate of the original
        transfer, not a newly supplied cost_per_min.

        Args:
            from_organization_id (int): ID of the child organization to revert from.
            minutes (float): Number of minutes to revert.

        Returns:
            dict: Response containing the new balances for both accounts.

        Raises:
            ValueError: If from_organization_id or minutes is not provided.
        """
        if from_organization_id is None:
            raise ValueError("from_organization_id is required.")
        if minutes is None:
            raise ValueError("minutes is required.")

        data = {
            'from_organization_id': from_organization_id,
            'minutes': minutes
        }
        return self.client.post("reseller/credits/revert", data=data)

    def credit_logs(self, page=1, page_size=30, start_date=None, end_date=None):
        """
        Get the credit transfer/revert log history.

        Args:
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 30).
            start_date (str): Filter logs from this date (optional).
            end_date (str): Filter logs up to this date (optional).

        Returns:
            dict: Response containing the list of credit log entries.
        """
        params = {
            'pageno': page,
            'pagesize': page_size
        }
        if start_date is not None:
            params['start_date'] = start_date
        if end_date is not None:
            params['end_date'] = end_date
        return self.client.get("reseller/credits/logs", params=params)

    def kyc_status(self, user_id):
        """
        Get the KYC status for a child user, per region.

        Args:
            user_id (int): ID of the child user.

        Returns:
            dict: Response containing per-region KYC status, including
                next_step to follow with submit_kyc_step.

        Raises:
            ValueError: If user_id is not provided.
        """
        if user_id is None:
            raise ValueError("user_id is required.")

        params = {'user_id': user_id}
        return self.client.get("reseller/kyc/status", params=params)

    def kyc_requirements(self, region):
        """
        Get the KYC requirements for a region.

        Args:
            region (str): Region to get KYC requirements for.

        Returns:
            dict: Response describing the required KYC steps for the region.

        Raises:
            ValueError: If region is not provided.
        """
        if not region:
            raise ValueError("region is required.")

        params = {'region': region}
        return self.client.get("reseller/kyc/requirements", params=params)

    def submit_kyc_step(self, step, user_id, region, **fields):
        """
        Submit one step of the KYC flow for a child user.

        The KYC flow is sequential: read the first step from kyc_status,
        submit it here, then follow next_step from each response into the
        next call to submit_kyc_step until the status is "completed".

        Args:
            step (str): KYC step name, e.g. register, verify-otp, resend-otp,
                verify-pan, aadhaar-otp, aadhaar-verify, verify-gst, skip-gst,
                preview, accept.
            user_id (int): ID of the child user.
            region (str): Region the KYC submission applies to.
            **fields: Additional fields required by the given step.

        Returns:
            dict: Response containing the updated KYC status and next_step.

        Raises:
            ValueError: If step, user_id, or region is not provided.
        """
        if not step:
            raise ValueError("step is required.")
        if user_id is None:
            raise ValueError("user_id is required.")
        if not region:
            raise ValueError("region is required.")

        data = {
            'user_id': user_id,
            'region': region
        }
        data.update(fields)

        return self.client.post("reseller/kyc/steps/{}".format(step), data=data)
