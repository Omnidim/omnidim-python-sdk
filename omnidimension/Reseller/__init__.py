import os


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

    def set_client_access(self, blocked, user_id=None, organization_id=None,
                          detach_numbers=None):
        """
        Block or restore a client, reversibly. Nothing is deleted.

        Args:
            blocked (bool): True to block, False to restore. Must be a real bool.
            user_id (int): The client user. Send this or organization_id, not both.
            organization_id (int): A client organization; every user in it is set.
            detach_numbers (bool): Also detach the organization's numbers from their
                agents (optional, only with organization_id and blocked=True).

        Returns:
            dict: Response with user_ids and, when numbers were detached, detached_numbers.

        Raises:
            ValueError: If blocked is not a bool, or not exactly one of user_id and
                organization_id is given.
        """
        if not isinstance(blocked, bool):
            raise ValueError("blocked must be True or False.")
        if (user_id is None) == (organization_id is None):
            raise ValueError("Send user_id or organization_id, not both and not neither.")

        data = {'blocked': blocked}
        if user_id is not None:
            data['user_id'] = user_id
        if organization_id is not None:
            data['organization_id'] = organization_id
        if detach_numbers is not None:
            data['detach_numbers'] = detach_numbers
        return self.client.post("reseller/users/access", data=data)

    def get_identity(self):
        """
        Read your brand and custom email server settings.

        Returns:
            dict: Response with has_identity, identity and smtp. The SMTP password
            is never returned.
        """
        return self.client.get("reseller/identity")

    def save_identity(self, company_name=None, platform_name=None, logo_url=None,
                      primary_color=None, real_email=None):
        """
        Set the brand your client organizations see. The first save creates it.

        Args:
            company_name (str): Company name, 1 to 60 characters of plain text (optional).
            platform_name (str): Brand name, 1 to 60 characters of plain text (optional).
            logo_url (str): Public URL of your logo (optional).
            primary_color (str): Hex colour such as "#1976d2" (optional).
            real_email (str): Sender and reply-to address on clients' emails (optional).

        Returns:
            dict: Response containing the full brand state.
        """
        data = {}
        if company_name is not None:
            data['company_name'] = company_name
        if platform_name is not None:
            data['platform_name'] = platform_name
        if logo_url is not None:
            data['logo_url'] = logo_url
        if primary_color is not None:
            data['primary_color'] = primary_color
        if real_email is not None:
            data['real_email'] = real_email

        return self.client.post("reseller/identity/save", data=data)

    def save_identity_smtp(self, host, port, username=None, password=None,
                           encryption=None, from_email=None):
        """
        Send your clients' emails through your own email server. The server is
        checked with a live login before it is saved. Save your brand first.

        Args:
            host (str): Email server host name.
            port (int): Email server port.
            username (str): Login name (optional).
            password (str): Login password. Leave out to keep the saved one (optional).
            encryption (str): "starttls" (default), "ssl" or "none" (optional).
            from_email (str): Address your clients' emails are sent from (optional).

        Returns:
            dict: Response containing the full brand state.

        Raises:
            ValueError: If host or port is not provided.
        """
        if not host:
            raise ValueError("host is required.")
        if port is None:
            raise ValueError("port is required.")

        data = {'host': host, 'port': port}
        if username is not None:
            data['username'] = username
        if password is not None:
            data['password'] = password
        if encryption is not None:
            data['encryption'] = encryption
        if from_email is not None:
            data['from_email'] = from_email

        return self.client.post("reseller/identity/smtp/save", data=data)

    def test_identity_smtp(self, host, port, username=None, password=None,
                           encryption=None, from_email=None):
        """
        Check a login to an email server. Nothing is saved.

        Args:
            host (str): Email server host name.
            port (int): Email server port.
            username (str): Login name (optional).
            password (str): Login password. Leave out to test the saved one (optional).
            encryption (str): "starttls" (default), "ssl" or "none" (optional).
            from_email (str): Address your clients' emails are sent from (optional).

        Returns:
            dict: Response with success True when the login works.

        Raises:
            ValueError: If host or port is not provided.
        """
        if not host:
            raise ValueError("host is required.")
        if port is None:
            raise ValueError("port is required.")

        data = {'host': host, 'port': port}
        if username is not None:
            data['username'] = username
        if password is not None:
            data['password'] = password
        if encryption is not None:
            data['encryption'] = encryption
        if from_email is not None:
            data['from_email'] = from_email

        return self.client.post("reseller/identity/smtp/test", data=data)

    def disable_identity_smtp(self):
        """
        Send your clients' emails back to the default sender. The saved server
        and its login are kept.

        Returns:
            dict: Response containing the full brand state.
        """
        return self.client.post("reseller/identity/smtp/disable")

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

    def kyc_requirements(self, region, carrier=None):
        """
        Get the KYC requirements for a region.

        Args:
            region (str): Region to get KYC requirements for.
            carrier (str): Carrier to get requirements for; valid values
                depend on region and are not fixed by this SDK. Carriers in
                the same region can have different requirements, so this
                decides the answer: an omitted or unknown carrier gets
                rejected by the API, which replies with the valid carriers
                for that region so you can retry (optional).

        Returns:
            dict: Response describing the required KYC steps for the region.

        Raises:
            ValueError: If region is not provided.
        """
        if not region:
            raise ValueError("region is required.")

        params = {'region': region}
        if carrier is not None:
            params['carrier'] = carrier
        return self.client.get("reseller/kyc/requirements", params=params)

    def submit_kyc_step(self, step, user_id, region, carrier=None, **fields):
        """
        Submit one step of the KYC flow for a child user.

        The KYC flow is sequential: read the first step from kyc_status,
        submit it here, then follow next_step from each response into the
        next call to submit_kyc_step until the status is "completed".

        Args:
            step (str): KYC step name for this carrier's flow. The valid
                step names and their order are not fixed by this SDK: they
                differ per carrier. Call kyc_requirements(region, carrier)
                to get the actual steps before submitting.
            user_id (int): ID of the child user.
            region (str): Region the KYC submission applies to.
            carrier (str): Carrier the KYC submission applies to; valid
                values depend on region and are not fixed by this SDK.
                Verification is per carrier: it decides which flow is
                walked and which record gets written (optional).
            **fields: Additional fields required by the given step. On a
                step whose method is "redirect", pass return_url to bring
                your client back to a page in your own app afterwards. A
                step whose method is "upload" takes a file: use
                upload_kyc_document for it.

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
        if carrier is not None:
            data['carrier'] = carrier
        data.update(fields)

        return self.client.post("reseller/kyc/steps/{}".format(step), data=data)

    def upload_kyc_document(self, step, user_id, region, document, filename=None,
                            carrier=None):
        """
        Upload a document for a KYC step whose method is "upload".

        Some carriers need a document after a check, such as the PAN card after
        PAN verification. next_step names the upload step when one is due, and
        kyc_requirements lists the accepted formats and size limit.

        Args:
            step (str): The upload step to run, for example "upload-pan".
            user_id (int): ID of the child user.
            region (str): Region the KYC submission applies to.
            document: A path to the file, its bytes, or a file opened in
                binary mode.
            filename (str): Name to send with the file, including its
                extension. Required when document is bytes; otherwise taken
                from the file (optional).
            carrier (str): Carrier the KYC submission applies to (optional).

        Returns:
            dict: Response containing the updated KYC status and next_step.

        Raises:
            ValueError: If step, user_id, region or document is missing, or
                document is bytes and no filename is given.
        """
        if not step:
            raise ValueError("step is required.")
        if user_id is None:
            raise ValueError("user_id is required.")
        if not region:
            raise ValueError("region is required.")
        if document is None:
            raise ValueError("document is required.")

        if isinstance(document, (bytes, bytearray)):
            if not filename:
                raise ValueError("filename is required when document is bytes.")
            content = bytes(document)
        elif isinstance(document, (str, os.PathLike)):
            with open(document, 'rb') as handle:
                content = handle.read()
            filename = filename or os.path.basename(document)
        else:
            content = document.read()
            filename = filename or os.path.basename(getattr(document, 'name', '') or '')
            if not filename:
                raise ValueError("filename is required when the file has no name.")

        data = {
            'user_id': user_id,
            'region': region
        }
        if carrier is not None:
            data['carrier'] = carrier

        return self.client.post("reseller/kyc/steps/{}".format(step), data=data,
                                files={'document': (filename, content)})

    def preview_client_release(self, organization_id):
        """
        What releasing a client would do, changing nothing. Call it before
        release_client. A release is refused while has_live_subscription is
        true.

        Args:
            organization_id (int): ID of the client organization.

        Returns:
            dict: Response with the balance, the share that returns, the
                numbers and the users.
        """
        return self.client.get("reseller/clients/release-preview",
                               params={'organization_id': organization_id})

    def release_client(self, organization_id):
        """
        Release a client for good. One-way: unlike set_client_access, it
        cannot be undone. It reverts the balance you funded, detaches the
        client's numbers, takes back the ones you bought, and retires its
        logins.

        Args:
            organization_id (int): ID of the client organization.

        Returns:
            dict: Response summarising what was released.

        Raises:
            ValueError: If organization_id is not provided.
        """
        if organization_id is None:
            raise ValueError("organization_id is required.")
        return self.client.post("reseller/clients/release",
                                data={'organization_id': organization_id})

    def issue_child_api_key(self, user_id, name):
        """
        Issue an API key for a user in one of your client organizations. The
        secret is in this response only; store it now, because no listing
        shows it again.

        Args:
            user_id (int): ID of the client user.
            name (str): Name for the key.

        Returns:
            dict: Response containing the key secret.
        """
        return self.client.post("reseller/users/api-keys",
                                data={'user_id': user_id, 'name': name})

    def revoke_child_api_key(self, user_id, api_key_id):
        """
        Revoke a client's API key. Pass the key's api_key_id, or 0 for the
        default key every account gets at signup. The key stops working on
        the next request.

        Args:
            user_id (int): ID of the client user.
            api_key_id (int): ID of the key, or 0 for the default key.

        Returns:
            dict: Response indicating success or failure.
        """
        return self.client.post("reseller/users/api-keys/revoke",
                                data={'user_id': user_id, 'api_key_id': api_key_id})
