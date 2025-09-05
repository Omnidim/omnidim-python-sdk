
class Call():
    def __init__(self, client):
        """
        Initialize the Agent client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client

    def dispatch_call(self, agent_id, to_number, from_number_id=None, call_context={}):
        """
        Dispatch a call to agent with the provided call context.

        Args:
            agent_id (int): id for the agent.
            to_number (string): valid phone number with country code.
            from_number_id(number)(optional): valid id of imported phone number api/v1/phone_number/list?
            call_context (dict): call context to be passed to agent during call.

        Returns:
            dict: Response from the API containing success.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Validate required inputs
        if not isinstance(agent_id, int):
            raise ValueError("agent id must be a integer.")
        if from_number_id and not isinstance(from_number_id, int):
            raise ValueError("from number id must be a integer.")
        if not isinstance(to_number, str) and to_number[0] != '+':
            raise ValueError("To Number must be a valid number and starts with + and country code.")            
        
        data = {
            "agent_id": agent_id,
            "to_number": to_number,
            "call_context": call_context,
            "from_number_id": from_number_id,
        }

        return self.client.post("calls/dispatch", data=data)
    

    def get_call_logs(self, page=1, page_size=30, agent_id=None, call_status=None):
        """
        Get all call logs for the authenticated user.
        
        Args:
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 30).
            agent_id (int): Filter by agent ID (optional).
            call_status (string): Filter by call status (optional).
        Returns:
            dict: Response containing the list of call logs .
        """
        params = {
            'pageno': page,
            'pagesize': page_size,
            'agentid': agent_id,
            'call_status': call_status,
        }
        return self.client.get("calls/logs", params=params)
    
    def get_call_log(self, call_log_id):
        """
        Get a specific agent by ID.

        Args:
            agent_id (int): The ID of the agent to retrieve.

        Returns:
            dict: Response containing the call log details.
        """
        return self.client.get(f"calls/logs/{call_log_id}")
    