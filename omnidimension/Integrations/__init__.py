
class Integrations():
    def __init__(self, client):
        """
        Initialize the Integrations client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client
        
    @staticmethod
    def get_integration_format_examples():
        """
        Returns examples of the expected format for different integration types.
        
        Returns:
            dict: A dictionary containing example formats for different integration types.
        """
        return {
            "custom_api": {
                "name": "Example API Integration",
                "description": "Integration with external service",
                "url": "http://api.example.com/endpoint",
                "method": "GET",
                "headers": [
                    {"key": "Authorization", "value": "Bearer token123"},
                    {"key": "Content-Type", "value": "application/json"}
                ],
                "integration_type": "custom_api",
                "query_params": [
                    {
                        "key": "user_id",
                        "description": "User identifier",
                        "type": "string",
                        "required": True,
                        "isLLMGenerated": False
                    }
                ],
                "body_params": [
                    {
                        "key": "message",
                        "description": "Message content",
                        "type": "string",
                        "required": True,
                        "isLLMGenerated": True
                    }
                ]
            },
            "cal": {
                "name": "Example Cal.com Integration",
                "description": "Integration with Cal.com calendar",
                "cal_api_key": "cal_api_key_12345",
                "cal_id": "cal_user_id",
                "cal_timezone": "America/New_York",
                "integration_type": "cal"
            }
        }

    def get_user_integrations(self):
        """
        Get all integrations available for the authenticated user.
        
        Returns:
            dict: Response containing the list of integrations.
        """
        return self.client.get("integrations")
        
    @staticmethod
    def _validate_integration_params(params_list, param_type):
        """
        Validate integration parameters format.
        
        Args:
            params_list: List of parameters to validate.
            param_type: Type of parameters being validated (headers, query_params, body_params).
            
        Raises:
            ValueError: If parameters don't follow the expected format.
        """
        if params_list is None:
            return
            
        if not isinstance(params_list, list):
            raise ValueError(f"{param_type} must be a list of dictionaries.")
            
        required_keys = {
            'headers': ['key', 'value'],
            'query_params': ['key'],
            'body_params': ['key']
        }
        
        for param in params_list:
            if not isinstance(param, dict):
                raise ValueError(f"Each {param_type} item must be a dictionary.")
                
            for key in required_keys.get(param_type, []):
                if key not in param:
                    raise ValueError(f"Each {param_type} item must contain a '{key}' field.")
                    
        # Additional validation for query_params and body_params
        if param_type in ['query_params', 'body_params']:
            for param in params_list:
                if 'type' in param and param['type'] not in ['string', 'number', 'boolean']:
                    raise ValueError(f"Parameter type must be one of: 'string', 'number', 'boolean'. Got: {param['type']}")
                    
                if 'required' in param and not isinstance(param['required'], bool):
                    raise ValueError("'required' field must be a boolean value.")
                    
                if 'isLLMGenerated' in param and not isinstance(param['isLLMGenerated'], bool):
                    raise ValueError("'isLLMGenerated' field must be a boolean value.")
    
    def create_custom_api_integration(self, name, url, method, description="", headers=None, 
                                      body_type=None, body_content=None, body_params=None, 
                                      query_params=None , stop_listening=False, request_timeout=10 ):
        """
        Create a custom API integration.
        
        Args:
            name (str): Name for the integration.
            url (str): URL for the API endpoint.
            method (str): HTTP method (GET, POST, PUT, DELETE, PATCH).
            description (str, optional): Description of the integration.
            headers (list, optional): Headers for the API request in the format:
                [
                    {"key": "header_name", "value": "header_value"},
                    ...
                ]
            body_type (str, optional): Body type (none, json, form).
            body_content (str, optional): Body content for the request.
            body_params (list, optional): Body parameters for the request in the format:
                [
                    {
                        "key": "param_name",
                        "description": "param_description",
                        "type": "string|number|boolean",
                        "required": true|false,
                        "isLLMGenerated": true|false
                    },
                    ...
                ]
            query_params (list, optional): Query parameters for the request in the format:
                [
                    {
                        "key": "param_name",
                        "description": "param_description",
                        "type": "string|number|boolean",
                        "required": true|false,
                        "isLLMGenerated": true|false
                    },
                    ...
                ]
            
        Returns:
            dict: Response from the API containing success status and integration ID.
            
        Raises:
            ValueError: If required fields are missing or invalid.
            
        Example:
            ```python
            # Create a custom API integration with headers and query parameters
            client.integrations.create_custom_api_integration(
                name="My API Integration",
                description="Integration with external service",
                url="http://api.example.com/endpoint",
                method="GET",
                headers=[
                    {"key": "Authorization", "value": "Bearer token123"},
                    {"key": "Content-Type", "value": "application/json"}
                ],
                query_params=[
                    {
                        "key": "user_id",
                        "description": "User identifier",
                        "type": "string",
                        "required": True,
                        "isLLMGenerated": False
                    }
                ]
            )
            ```
        """
        # Validate required inputs
        if not name or not url or not method:
            raise ValueError("Name, URL, and method are required fields.")
        
        # Validate parameters format
        self._validate_integration_params(headers, 'headers')
        self._validate_integration_params(query_params, 'query_params')
        self._validate_integration_params(body_params, 'body_params')
        
        data = {
            "name": name,
            "url": url,
            "method": method,
            "description": description,
            "integration_type": "custom_api",
            "stop_listening": stop_listening,
            "request_timeout": request_timeout
        }
        
        # Add optional fields if provided
        if headers is not None:
            data["headers"] = headers
        
        if body_type is not None:
            data["body_type"] = body_type
        
        if body_content is not None:
            data["body_content"] = body_content
        
        if body_params is not None:
            data["body_params"] = body_params
        
        if query_params is not None:
            data["query_params"] = query_params
        
        return self.client.post("integrations/custom-api", data=data)
    
    def create_cal_integration(self, name, cal_api_key, cal_id, cal_timezone, description=""):
        """
        Create a Cal.com integration.
        
        Args:
            name (str): Name for the integration.
            cal_api_key (str): Cal.com API key.
            cal_id (str): Cal.com ID.
            cal_timezone (str): Cal.com timezone.
            description (str, optional): Description of the integration.
            
        Returns:
            dict: Response from the API containing success status and integration ID.
            
        Raises:
            ValueError: If required fields are missing or invalid.
            
        Example:
            ```python
            # Create a Cal.com integration
            client.integrations.create_cal_integration(
                name="My Calendar Integration",
                description="Integration with Cal.com calendar",
                cal_api_key="cal_api_key_12345",
                cal_id="cal_user_id",
                cal_timezone="America/New_York"
            )
            ```
        """
        # Validate required inputs
        if not name or not cal_api_key or not cal_id or not cal_timezone:
            raise ValueError("Name, Cal.com API key, Cal.com ID, and Cal.com timezone are required fields.")
        
        # Validate input types
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if not isinstance(cal_api_key, str):
            raise ValueError("Cal.com API key must be a string.")
        if not isinstance(cal_id, str):
            raise ValueError("Cal.com ID must be a string.")
        if not isinstance(cal_timezone, str):
            raise ValueError("Cal.com timezone must be a string.")
            
        data = {
            "name": name,
            "cal_api_key": cal_api_key,
            "cal_id": cal_id,
            "cal_timezone": cal_timezone,
            "description": description,
            "integration_type": "cal"
        }
        
        return self.client.post("integrations/cal", data=data)
    
    def create_integration_from_json(self, integration_data):
        """
        Create an integration directly from a complete JSON object.
        
        This method is useful when you have a complete integration configuration
        in the expected format and want to create the integration in one call.
        
        Args:
            integration_data (dict): Complete integration data in the expected format.
                Must include 'integration_type' field and all required fields for that type.
                
        Returns:
            dict: Response from the API containing success status and integration ID.
            
        Raises:
            ValueError: If required fields are missing or invalid.
            
        Example:
            ```python
            # Create a custom API integration from a complete JSON object
            integration_data = {
                "name": "My API Integration",
                "description": "Integration with external service",
                "url": "http://api.example.com/endpoint",
                "method": "GET",
                "headers": [
                    {"key": "Authorization", "value": "Bearer token123"}
                ],
                "integration_type": "custom_api",
                "query_params": [
                    {
                        "key": "user_id",
                        "description": "User identifier",
                        "type": "string",
                        "required": True,
                        "isLLMGenerated": False
                    }
                ]
            }
            client.integrations.create_integration_from_json(integration_data)
            ```
        """
        if not integration_data or not isinstance(integration_data, dict):
            raise ValueError("Integration data must be a non-empty dictionary.")
            
        if 'integration_type' not in integration_data:
            raise ValueError("Integration data must include 'integration_type' field.")
            
        integration_type = integration_data.get('integration_type')
        
        # Validate based on integration type
        if integration_type == 'custom_api':
            # Required fields for custom API
            required_fields = ['name', 'url', 'method']
            for field in required_fields:
                if field not in integration_data:
                    raise ValueError(f"'{field}' is required for custom API integration.")
                    
            # Validate parameters if present
            if 'headers' in integration_data:
                self._validate_integration_params(integration_data['headers'], 'headers')
            if 'query_params' in integration_data:
                self._validate_integration_params(integration_data['query_params'], 'query_params')
            if 'body_params' in integration_data:
                self._validate_integration_params(integration_data['body_params'], 'body_params')
                
            endpoint = "integrations/custom-api"
            
        elif integration_type == 'cal':
            # Required fields for Cal.com
            required_fields = ['name', 'cal_api_key', 'cal_id', 'cal_timezone']
            for field in required_fields:
                if field not in integration_data:
                    raise ValueError(f"'{field}' is required for Cal.com integration.")
                    
            endpoint = "integrations/cal"
            
        else:
            raise ValueError(f"Unsupported integration type: {integration_type}")
            
        return self.client.post(endpoint, data=integration_data)
        
    def get_agent_integrations(self, agent_id):
        """
        Get all integrations for a specific agent.
        
        Args:
            agent_id (int): ID of the agent to get integrations for.
            
        Returns:
            dict: Response containing the list of integrations for the agent.
            
        Raises:
            ValueError: If agent_id is not provided or invalid.
        """
        if not isinstance(agent_id, int) or agent_id <= 0:
            raise ValueError("Agent ID must be a positive integer.")
            
        return self.client.get(f"agents/{agent_id}/integrations")
    
    def add_integration_to_agent(self, agent_id, integration_id):
        """
        Add an existing integration to an agent.
        
        Args:
            agent_id (int): ID of the agent.
            integration_id (int): ID of the integration to add.
            
        Returns:
            dict: Response containing the result of the operation.
            
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if not isinstance(agent_id, int) or agent_id <= 0:
            raise ValueError("Agent ID must be a positive integer.")
            
        if not isinstance(integration_id, int) or integration_id <= 0:
            raise ValueError("Integration ID must be a positive integer.")
            
        data = {
            "integration_id": integration_id
        }
        
        return self.client.post(f"agents/{agent_id}/integrations", data=data)
    
    def remove_integration_from_agent(self, agent_id, integration_id):
        """
        Remove an integration from an agent.
        
        Args:
            agent_id (int): ID of the agent.
            integration_id (int): ID of the integration to remove.
            
        Returns:
            dict: Response containing the result of the operation.
            
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if not isinstance(agent_id, int) or agent_id <= 0:
            raise ValueError("Agent ID must be a positive integer.")
            
        if not isinstance(integration_id, int) or integration_id <= 0:
            raise ValueError("Integration ID must be a positive integer.")
            
        return self.client.delete(f"agents/{agent_id}/integrations/{integration_id}")
    