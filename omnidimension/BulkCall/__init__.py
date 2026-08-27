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
                         is_scheduled=False, scheduled_datetime=None, timezone='UTC',
                         retry_config=None, enabled_reschedule_call=False,
                         bot_id=None, save_as_draft=False, call_conditions=None,
                         rotation=None, concurrent_call_limit=None):
        """
        Create a new bulk call campaign.

        Args:
            name (str): Name of the bulk call campaign.
            contact_list (list): List of contact dictionaries with phone_number and extra_data.
            phone_number_id (int): ID of the phone number to use for the calls.
            is_scheduled (bool): Whether the call is scheduled for later (default: False).
            scheduled_datetime (str): Scheduled datetime in format "YYYY-MM-DD HH:MM:SS" (required if is_scheduled=True).
            timezone (str): Timezone for the scheduled datetime (default: 'UTC').
            retry_config (dict): Auto-retry configuration with keys: auto_retry, auto_retry_schedule, retry_schedule_days, retry_schedule_hours, retry_limit.
            enabled_reschedule_call (bool): Enable call rescheduling (default: False).
            bot_id (int, optional): ID of the agent to run the calls with.
            save_as_draft (bool): Create the campaign as a draft instead of dispatching (default: False).
            call_conditions (list, optional): List of condition dictionaries with keys: column, operator, value.
            rotation (dict, optional): Number rotation configuration with keys:
                - numbers (list): List of {'phone_number_id': int, 'sequence': int (optional)}.
                - strategy (str, optional): Rotation strategy.
                - calls_per_number (int, optional): Calls before rotating to the next number.
                - health_threshold (float, optional): Health score below which a number is skipped.
                - fallback (dict, optional): Fallback behaviour configuration.
            concurrent_call_limit (int, optional): Maximum simultaneous calls for the campaign.

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
        try:
            phone_number_id = int(phone_number_id)
        except (TypeError, ValueError):
            raise ValueError("phone_number_id must be an integer or a numeric string")
        
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
            'timezone': timezone,
            'enabled_reschedule_call': enabled_reschedule_call
        }

        if is_scheduled:
            data['scheduled_datetime'] = scheduled_datetime

        if retry_config:
            data['retry_config'] = retry_config

        if bot_id is not None:
            if not isinstance(bot_id, int):
                raise ValueError("bot_id must be an integer")
            data['bot_id'] = bot_id

        if save_as_draft:
            data['save_as_draft'] = True

        if call_conditions is not None:
            if not isinstance(call_conditions, list):
                raise ValueError("call_conditions must be a list of dictionaries")
            data['call_conditions'] = call_conditions

        if rotation is not None:
            if not isinstance(rotation, dict):
                raise ValueError("rotation must be a dictionary")
            data['rotation'] = rotation

        if concurrent_call_limit is not None:
            if not isinstance(concurrent_call_limit, int) or concurrent_call_limit < 1:
                raise ValueError("concurrent_call_limit must be an integer >= 1")
            data['concurrent_call_limit'] = concurrent_call_limit

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

    def add_contact(self, bulk_call_id, to_number, custom_variables=None, metadata=None):
        """
        Add a single contact to an existing bulk call campaign.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.
            to_number (str): Phone number to call.
            custom_variables (dict, optional): Custom variables for this contact.
            metadata (dict, optional): Metadata for this contact.

        Returns:
            dict: Response containing the added contact details.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if not isinstance(to_number, str) or not to_number.strip():
            raise ValueError("to_number must be a non-empty string")

        data = {'to_number': to_number}
        if custom_variables is not None:
            data['custom_variables'] = custom_variables
        if metadata is not None:
            data['metadata'] = metadata

        return self.client.post(f"calls/bulk_call/{bulk_call_id}/add_contact", data=data)

    def add_contacts(self, bulk_call_id, contacts):
        """
        Add multiple contacts to an existing bulk call campaign.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.
            contacts (list): List of contact dictionaries, each with a 'to_number' field
                and optional 'custom_variables' and 'metadata'. Maximum 1000 per request.

        Returns:
            dict: Response containing the added contacts.

        Raises:
            ValueError: If contacts is empty, exceeds 1000 entries, or an entry is invalid.
        """
        if not isinstance(contacts, list) or not contacts:
            raise ValueError("contacts must be a non-empty list")
        if len(contacts) > 1000:
            raise ValueError("contacts must contain at most 1000 entries per request")
        for i, contact in enumerate(contacts):
            if not isinstance(contact, dict):
                raise ValueError(f"contacts[{i}] must be a dictionary")
            if 'to_number' not in contact:
                raise ValueError(f"contacts[{i}] must contain 'to_number' field")

        return self.client.post(f"calls/bulk_call/{bulk_call_id}/add_contacts", data={'contacts': contacts})

    def start_bulk_call(self, bulk_call_id):
        """
        Start a draft bulk call campaign.

        Args:
            bulk_call_id (int): ID of the bulk call campaign to start.

        Returns:
            dict: Response containing the start result.
        """
        return self.client.post(f"calls/bulk_call/{bulk_call_id}/start", data={})

    def update_concurrency(self, bulk_call_id, concurrent_call_limit):
        """
        Update the concurrent call limit of a bulk call campaign.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.
            concurrent_call_limit (int): Maximum simultaneous calls (must be >= 1).

        Returns:
            dict: Response containing the update result.

        Raises:
            ValueError: If concurrent_call_limit is not an integer >= 1.
        """
        if not isinstance(concurrent_call_limit, int) or concurrent_call_limit < 1:
            raise ValueError("concurrent_call_limit must be an integer >= 1")

        return self.client.put(f"calls/bulk_call/{bulk_call_id}/concurrency",
                               data={'concurrent_call_limit': concurrent_call_limit})

    def manual_retry(self, bulk_call_id):
        """
        Manually retry the failed calls of a bulk call campaign.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.

        Returns:
            dict: Response containing the retry result.
        """
        return self.client.post(f"calls/bulk_call/{bulk_call_id}/manual_retry", data={})

    def get_bulk_call_lines(self, bulk_call_id, pagesize=None, cursor=None, call_status=None,
                            interaction_status=None, search=None, include_total=None):
        """
        Get the call lines of a bulk call campaign with cursor pagination and filtering.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.
            pagesize (int, optional): Number of lines per page (maximum 150).
            cursor (str, optional): Cursor from a previous response for the next page.
            call_status (str, optional): Filter by call status.
            interaction_status (str, optional): Filter by interaction status.
            search (str, optional): Search term to filter lines.
            include_total (bool, optional): Include the total line count in the response.

        Returns:
            dict: Response containing the call lines.

        Raises:
            ValueError: If pagesize exceeds 150.
        """
        if pagesize is not None and pagesize > 150:
            raise ValueError("pagesize must be at most 150")

        params = {}
        if pagesize is not None:
            params['pagesize'] = pagesize
        if cursor is not None:
            params['cursor'] = cursor
        if call_status is not None:
            params['call_status'] = call_status
        if interaction_status is not None:
            params['interaction_status'] = interaction_status
        if search is not None:
            params['search'] = search
        if include_total:
            params['include_total'] = 'true'

        return self.client.get(f"calls/bulk_call/{bulk_call_id}/lines", params=params)

    def get_live_status(self, bulk_call_id):
        """
        Get the live status of a running bulk call campaign.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.

        Returns:
            dict: Response containing the live campaign status.
        """
        return self.client.get(f"bulk-call/{bulk_call_id}/live-status")

    def list_rotation_numbers(self, bulk_call_id):
        """
        List the phone numbers assigned to a bulk call campaign's rotation.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.

        Returns:
            dict: Response containing the rotation number assignments.
        """
        return self.client.get(f"calls/bulk_call/{bulk_call_id}/numbers")

    def add_rotation_number(self, bulk_call_id, phone_number_id):
        """
        Add a phone number to a bulk call campaign's rotation.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.
            phone_number_id (int): ID of the phone number to add.

        Returns:
            dict: Response containing the new rotation assignment.

        Raises:
            ValueError: If phone_number_id is not an integer.
        """
        try:
            phone_number_id = int(phone_number_id)
        except (TypeError, ValueError):
            raise ValueError("phone_number_id must be an integer or a numeric string")

        return self.client.post(f"calls/bulk_call/{bulk_call_id}/numbers",
                                data={'phone_number_id': phone_number_id})

    def set_rotation_number_active(self, bulk_call_id, assignment_id, is_active):
        """
        Enable or disable a rotation number assignment.

        Args:
            bulk_call_id (int): ID of the bulk call campaign.
            assignment_id (int): ID of the rotation number assignment.
            is_active (bool): Whether the number should be active in the rotation.

        Returns:
            dict: Response containing the updated assignment.

        Raises:
            ValueError: If is_active is not a boolean.
        """
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be a boolean")

        return self.client.put(f"calls/bulk_call/{bulk_call_id}/numbers/{assignment_id}",
                               data={'is_active': is_active})
