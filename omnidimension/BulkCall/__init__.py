class BulkCall():
    def __init__(self, client):
        """
        Initialize the BulkCall client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client

    def fetch_bulk_calls(self, page=1, page_size=10, status=None):
        """
        Fetch all bulk calls with optional filtering and pagination.
        
        Args:
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 10).
            status (str): Filter by bulk call status (optional).
            
        Returns:
            dict: Response containing the list of bulk calls.
        """
        params = {
            'pageno': page,
            'pagesize': page_size
        }
        if status:
            params['status'] = status
            
        return self.client.get("calls/bulk_call", params=params)

    def create_bulk_calls(self, name, contact_list, phone_number_id, 
                         is_scheduled=False, scheduled_datetime=None, timezone='UTC'):
        """
        Create a new bulk call campaign.
        
        Args:
            name (str): Name of the bulk call campaign.
            contact_list (list): List of contact dictionaries with phone_number and extra_data.
            phone_number_id (int): ID of the phone number to use for the calls.
            is_scheduled (bool): Whether the call is scheduled for later (default: False).
            scheduled_datetime (str): Scheduled datetime in format "YYYY-MM-DD HH:MM:SS" (required if is_scheduled=True).
            timezone (str): Timezone for the scheduled datetime (default: 'UTC').
            
        Returns:
            dict: Response containing the created bulk call details.
            
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Validate required inputs
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(contact_list, list) or not contact_list:
            raise ValueError("contact_list must be a non-empty list")
        if not isinstance(phone_number_id, int):
            raise ValueError("phone_number_id must be an integer")
        
        # Validate contact list format
        for i, contact in enumerate(contact_list):
            if not isinstance(contact, dict):
                raise ValueError(f"contact_list[{i}] must be a dictionary")
            if 'phone_number' not in contact:
                raise ValueError(f"contact_list[{i}] must contain 'phone_number' field")
            if not isinstance(contact['phone_number'], str) or not contact['phone_number'].startswith('+'):
                raise ValueError(f"contact_list[{i}]['phone_number'] must be a string starting with '+'")
        
        if is_scheduled and not scheduled_datetime:
            raise ValueError("scheduled_datetime is required when is_scheduled is True")
        
        data = {
            'name': name,
            'contact_list': contact_list,
            'phone_number_id': phone_number_id,
            'is_scheduled': is_scheduled,
            'timezone': timezone
        }
        
        if is_scheduled:
            data['scheduled_datetime'] = scheduled_datetime
            
        return self.client.post("calls/bulk_call/create", data=data)

    def bulk_calls_actions(self, bulk_call_id, action, new_timezone=None, new_scheduled_datetime=None):
        """
        Perform actions on a bulk call (pause, resume, reschedule).
        
        Args:
            bulk_call_id (int): ID of the bulk call to modify.
            action (str): Action to perform ('pause', 'resume', or 'reschedule').
            new_timezone (str): New timezone for reschedule action (optional).
            new_scheduled_datetime (str): New scheduled datetime for reschedule action (required for reschedule).
            
        Returns:
            dict: Response containing the action result.
            
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if action not in ['pause', 'resume', 'reschedule']:
            raise ValueError("action must be 'pause', 'resume', or 'reschedule'")
        
        if action == 'reschedule' and not new_scheduled_datetime:
            raise ValueError("new_scheduled_datetime is required for reschedule action")
        
        data = {
            'action': action
        }
        
        if new_timezone:
            data['new_timezone'] = new_timezone
        if new_scheduled_datetime:
            data['new_scheduled_datetime'] = new_scheduled_datetime
            
        return self.client.put(f"calls/bulk_call/{bulk_call_id}", data=data)

    def cancel_bulk_calls(self, bulk_call_id):
        """
        Cancel a bulk call campaign.
        
        Args:
            bulk_call_id (int): ID of the bulk call to cancel.
            
        Returns:
            dict: Response containing the cancellation result.
        """
        return self.client.delete(f"calls/bulk_call/{bulk_call_id}")

    def detail_bulk_calls(self, bulk_call_id):
        """
        Get detailed information about a specific bulk call campaign.
        
        Args:
            bulk_call_id (int): ID of the bulk call to retrieve.
            
        Returns:
            dict: Response containing the bulk call details and contact list.
        """
        return self.client.get(f"calls/bulk_call/{bulk_call_id}")
