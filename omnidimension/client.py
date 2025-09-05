import requests
import json
from urllib.parse import urljoin

class APIError(Exception):
    """Exception raised for API errors."""
    def __init__(self, status_code, message, response=None):
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"API Error ({status_code}): {message}")

class Client(object):
    def __init__(self, api_key, base_url='https://backend.omnidim.io/api/v1'):
        """
        Initialize the OmniClient with API key and base URL.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL of the API.
        """
        if not api_key:
            raise ValueError("API key is required.")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        print(self.base_url)
        # Lazy-loaded domain clients
        self._agent = None
        self._bulk_call = None
        self._call = None
        self._integrations = None
        self._knowledge_base = None
        self._phone_number = None
        self._simulation = None
        
        # Verify API key format (basic validation)
        if not isinstance(api_key, str) or len(api_key.strip()) < 8:
            raise ValueError("API key appears to be invalid. Please check your credentials.")

    def request(self, method, endpoint, params=None, headers=None, data=None, json_data=None):
        """
        Universal request method to handle all API requests.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path (without base URL)
            params (dict, optional): URL parameters
            headers (dict, optional): HTTP headers
            data (dict, optional): Form data
            json_data (dict, optional): JSON data

        Returns:
            dict: Response with status code and JSON data

        Raises:
            APIError: If the API returns an error status code
            requests.exceptions.RequestException: For network-related errors
        """
        # Prepare request
        headers = headers or {}
        params = params or {}
        method = method.upper()
        
        # Add authorization header
        headers.setdefault('Authorization', f'Bearer {self.api_key}')
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('Accept', 'application/json')
        
        # Build full URL
        url = self.base_url + '/' + endpoint.lstrip('/')
        print("->",url, self.base_url, endpoint)
        try:
            # Make the request
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                data=data,
                json=json_data
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Process response based on method
            if method == "DELETE":
                json_response = {}
            else:
                json_response = response.json() if response.content else {}
                
            return {
                "status": response.status_code,
                "json": json_response
            }
            
        except requests.exceptions.HTTPError as e:
            # Handle API errors with response
            error_message = "Unknown error"
            error_data = {}
            
            try:
                error_data = e.response.json()
                error_message = error_data.get('error_description', error_data.get('error', str(e)))
            except (ValueError, AttributeError, KeyError):
                error_message = str(e)
                
            raise APIError(
                status_code=e.response.status_code,
                message=error_message,
                response=error_data
            )
            
        except requests.exceptions.RequestException as e:
            # Handle network errors
            raise APIError(
                status_code=0,
                message=f"Network error: {str(e)}"
            )
    
    # Convenience methods for different HTTP methods
    def get(self, endpoint, params=None, headers=None):
        """Make a GET request to the API."""
        return self.request("GET", endpoint, params=params, headers=headers)
    
    def post(self, endpoint, data=None, params=None, headers=None):
        """Make a POST request to the API."""
        return self.request("POST", endpoint, params=params, headers=headers, json_data=data)
    
    def put(self, endpoint, data=None, params=None, headers=None):
        """Make a PUT request to the API."""
        return self.request("PUT", endpoint, params=params, headers=headers, json_data=data)
    
    def delete(self, endpoint, params=None, headers=None):
        """Make a DELETE request to the API."""
        return self.request("DELETE", endpoint, params=params, headers=headers)
    
    # Domain-specific clients (lazy-loaded)
    @property
    def agent(self):
        """Get the Agent client."""
        if self._agent is None:
            from .Agent import Agent
            self._agent = Agent(self)
        return self._agent

    @property
    def bulk_call(self):
        """Get the BulkCall client."""
        if self._bulk_call is None:
            from .BulkCall import BulkCall
            self._bulk_call = BulkCall(self)
        return self._bulk_call

    @property
    def call(self):
        """Get the Callback client."""
        if self._call is None:
            from .Call import Call
            self._call = Call(self)
        return self._call

    @property
    def integrations(self):
        """Get the Integrations client."""
        if self._integrations is None:
            from .Integrations import Integrations
            self._integrations = Integrations(self)
        return self._integrations
        
    @property
    def knowledge_base(self):
        """Get the KnowledgeBase client."""
        if self._knowledge_base is None:
            from .KnowledgeBase import KnowledgeBase
            self._knowledge_base = KnowledgeBase(self)
        return self._knowledge_base
        
    @property
    def phone_number(self):
        """Get the PhoneNumber client."""
        if self._phone_number is None:
            from .PhoneNumber import PhoneNumber
            self._phone_number = PhoneNumber(self)
        return self._phone_number

    @property
    def simulation(self):
        """Get the Simulation client."""
        if self._simulation is None:
            from .Simulation import Simulation
            self._simulation = Simulation(self)
        return self._simulation