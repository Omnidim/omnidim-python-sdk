class PhoneNumber():
    def __init__(self, client):
        """
        Initialize the PhoneNumber client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client

    def list(self, page=1, page_size=30):
        """
        Get all phone numbers for the authenticated user.
        
        Args:
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 30).
            
        Returns:
            dict: Response containing the list of phone numbers.
        """
        params = {
            'pageno': page,
            'pagesize': page_size
        }
        return self.client.get("phone_number/list", params=params)
    
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

    def import_twilio_number(self, phone_number, account_sid, account_token, name=None):
        """
        Import an existing Twilio number to your account.

        Args:
            phone_number (str): The Twilio phone number to import.
            account_sid (str): Twilio Account SID.
            account_token (str): Twilio Auth Token.
            name (str, optional): Custom name for the phone number.

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        if not phone_number:
            raise ValueError("phone_number is required.")
        if not account_sid:
            raise ValueError("account_sid is required.")
        if not account_token:
            raise ValueError("account_token is required.")

        data = {
            "phone_number": phone_number,
            "account_sid": account_sid,
            "account_token": account_token
        }

        if name:
            data["name"] = name

        return self.client.post("phone_number/import/twilio", data=data)

    def import_exotel_number(self, exotel_phone_number, exotel_api_key, exotel_api_token,
                           exotel_subdomain, exotel_account_sid, exotel_app_id, name=None):
        """
        Import an existing Exotel number to your account.

        Args:
            exotel_phone_number (str): The Exotel phone number to import.
            exotel_api_key (str): Exotel API key.
            exotel_api_token (str): Exotel API token.
            exotel_subdomain (str): Exotel subdomain.
            exotel_account_sid (str): Exotel Account SID.
            exotel_app_id (str): Exotel App ID.
            name (str, optional): Custom name for the phone number.

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        if not exotel_phone_number:
            raise ValueError("exotel_phone_number is required.")
        if not exotel_api_key:
            raise ValueError("exotel_api_key is required.")
        if not exotel_api_token:
            raise ValueError("exotel_api_token is required.")
        if not exotel_subdomain:
            raise ValueError("exotel_subdomain is required.")
        if not exotel_account_sid:
            raise ValueError("exotel_account_sid is required.")
        if not exotel_app_id:
            raise ValueError("exotel_app_id is required.")

        data = {
            "exotel_phone_number": exotel_phone_number,
            "exotel_api_key": exotel_api_key,
            "exotel_api_token": exotel_api_token,
            "exotel_subdomain": exotel_subdomain,
            "exotel_account_sid": exotel_account_sid,
            "exotel_app_id": exotel_app_id
        }

        if name:
            data["name"] = name

        return self.client.post("phone_number/import/exotel", data=data)

    def import_twilio_whatsapp_number(self, phone_number, account_sid, account_token, name=None):
        """
        Import an existing Twilio WhatsApp number to your account.

        Args:
            phone_number (str): The Twilio WhatsApp phone number to import.
            account_sid (str): Twilio Account SID.
            account_token (str): Twilio Auth Token.
            name (str, optional): Custom name for the phone number.

        Returns:
            dict: Response indicating success or failure.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        if not phone_number:
            raise ValueError("phone_number is required.")
        if not account_sid:
            raise ValueError("account_sid is required.")
        if not account_token:
            raise ValueError("account_token is required.")

        data = {
            "phone_number": phone_number,
            "account_sid": account_sid,
            "account_token": account_token
        }

        if name:
            data["name"] = name

        return self.client.post("phone_number/import/twilio-whatsapp", data=data)