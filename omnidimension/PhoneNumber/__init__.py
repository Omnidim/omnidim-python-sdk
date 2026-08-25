class PhoneNumber():
    def __init__(self, client):
        """
        Initialize the PhoneNumber client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client

    def list(self, page=1, page_size=30, user_id=None):
        """
        Get all phone numbers for the authenticated user.

        Args:
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 30).
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the list of phone numbers.
        """
        params = {
            'pageno': page,
            'pagesize': page_size
        }
        if user_id is not None:
            params['user_id'] = user_id
        return self.client.get("phone_number/list", params=params)

    def search(self, region, pattern=None, page=1, limit=20, user_id=None):
        """
        Search for phone numbers available for purchase in a region.

        Args:
            region (str): Region to search for available numbers.
            pattern (str): Number pattern to match (optional).
            page (int): Page number for pagination (default: 1).
            limit (int): Number of items per page (default: 20).
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing matching phone numbers.

        Raises:
            ValueError: If region is not provided.
        """
        if not region:
            raise ValueError("region is required.")

        params = {'region': region}
        if pattern is not None:
            params['pattern'] = pattern
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if user_id is not None:
            params['user_id'] = user_id
        return self.client.get("phone_number/search", params=params)

    def purchase(self, region, phone_number, user_id=None, idempotency_key=None):
        """
        Purchase a phone number in a region.

        Args:
            region (str): Region of the phone number.
            phone_number (str): The phone number to purchase.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).
            idempotency_key (str): Key to safely retry the purchase without
                double-charging; a replayed key returns the original order
                with "replayed": true (optional).

        Returns:
            dict: Response containing the purchase details.

        Raises:
            ValueError: If region or phone_number is not provided.
        """
        if not region:
            raise ValueError("region is required.")
        if not phone_number:
            raise ValueError("phone_number is required.")

        data = {
            'region': region,
            'phone_number': phone_number
        }
        if user_id is not None:
            data['user_id'] = user_id

        # Client.post already accepts and forwards headers, so no client.py change is needed.
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self.client.post("phone_number/purchase", data=data, headers=headers)

    def release(self, phone_number, user_id=None):
        """
        Release a previously purchased phone number.

        Args:
            phone_number (str): The phone number to release.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If phone_number is not provided.
        """
        if not phone_number:
            raise ValueError("phone_number is required.")

        data = {'phone_number': phone_number}
        if user_id is not None:
            data['user_id'] = user_id
        return self.client.post("phone_number/release", data=data)

    def attach(self, phone_number_id, agent_id):
        """
        Attach a phone number to an agent.
        
        Args:
            phone_number_id (int): ID of the phone number to attach.
            agent_id (int): ID of the agent to attach the phone number to.
            
        Returns:
            dict: Response indicating success or failure.
            
        Raises:
            ValueError: If phone_number_id or agent_id is not an integer.
        """
        if not isinstance(phone_number_id, int):
            raise ValueError("phone_number_id must be an integer.")
        if not isinstance(agent_id, int):
            raise ValueError("agent_id must be an integer.")
            
        data = {
            "phone_number_id": phone_number_id,
            "agent_id": agent_id
        }
        
        return self.client.post("phone_number/attach", data=data)
    
    def detach(self, phone_number_id):
        """
        Detach a phone number from any agent it's attached to.
        
        Args:
            phone_number_id (int): ID of the phone number to detach.
            
        Returns:
            dict: Response indicating success or failure.
            
        Raises:
            ValueError: If phone_number_id is not an integer.
        """
        if not isinstance(phone_number_id, int):
            raise ValueError("phone_number_id must be an integer.")
            
        data = {
            "phone_number_id": phone_number_id
        }
        
        return self.client.post("phone_number/detach", data=data)