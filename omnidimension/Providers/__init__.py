from ..client import APIError

class Providers:
    """
    Client for interacting with the OmniDim Providers API endpoints.
    """

    def __init__(self, client):
        """
        Initialize the Providers client with a reference to the main API client.

        Args:
            client: The main API client instance.
        """
        self.client = client

    def list_llms(self):
        """
        Fetch all LLM providers.

        Returns:
            dict: Response containing the list of LLM providers with 'llms' and 'total' keys.
        """
        response = self.client.get("providers/llms")
        return response['json']

    def list_voices(self, provider=None, search=None, language=None, accent=None,
                gender=None, page=1, page_size=30):
        """
        Fetch all voice providers with advanced filtering and pagination.

        Args:
            provider (str): Filter by specific TTS provider (e.g., 'eleven_labs', 'google', 'deepgram').
                        Only 'eleven_labs' supports advanced filtering (search, language, accent, gender).
            search (str): Search term for voice name/description (ElevenLabs only).
            language (str): Language filter (ElevenLabs only).
            accent (str): Accent filter (ElevenLabs only).
            gender (str): Gender filter ('male' or 'female', ElevenLabs only).
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 30, max: 100).

        Returns:
            dict: Response containing the list of voices with 'voices', 'total', 'page',
                'page_size', and 'filters_applied' keys.
        """
        # basic parameter validation for immediate feedback
        if not isinstance(page, int) or page < 1:
            raise ValueError("page must be a positive integer (1 or greater)")
        if not isinstance(page_size, int) or page_size < 1 or page_size > 100:
            raise ValueError("page_size must be an integer between 1 and 100")
        if gender and gender not in ['male', 'female']:
            raise ValueError("gender must be 'male' or 'female'")

        # client-side validation for filter limitations
        if provider and provider != 'eleven_labs':
            advanced_filters = [search, language, accent, gender]
            if any(filter_val is not None for filter_val in advanced_filters):
                raise ValueError(
                    f"Advanced filtering (search, language, accent, gender) is only supported "
                    f"for provider 'eleven_labs'. Provider '{provider}' only supports pagination."
                )

        params = {}

        # pagination parameters (integers)
        params['page'] = page
        params['page_size'] = page_size

        # optional string parameters
        if provider:
            params['provider'] = provider
        if search:
            params['search'] = search
        if language:
            params['language'] = language
        if accent:
            params['accent'] = accent
        if gender:
            params['gender'] = gender

        # let backend handle validation of unknown providers, invalid languages, etc.
        # but catch common user-facing issues here
        
        try:
            response = self.client.get("providers/voices", params=params)
            return response['json']
        except APIError as e:
            # handle rate limiting 
            if e.status_code == 429:
                retry_after = getattr(e, 'response', {}).get('retry_after', 60)
                raise ValueError(f"Rate limit exceeded. Please wait {retry_after} seconds before trying again.")
            # handle authentication errors
            elif e.status_code == 401:
                raise ValueError("Authentication failed. Please check your API key.")
            # handle not found errors
            elif e.status_code == 404:
                raise ValueError("The requested provider endpoint was not found.")
            # let other API errors fill up with backend's message
            else:
                raise ValueError(f"API Error: {e.message}")

    def list_tts(self):
        """
        Fetch all TTS providers.

        Returns:
            dict: Response containing the list of TTS providers with 'tts' and 'total' keys.
        """
        response = self.client.get("providers/tts")
        return response['json']

    def list_stt(self):
        """
        Fetch all STT providers.

        Returns:
            dict: Response containing the list of STT providers with 'stt' and 'total' keys.
        """
        response = self.client.get("providers/stt")
        return response['json']

    def list_all(self):
        """
        Fetch all providers (services and voices) in a comprehensive response.

        Returns:
            dict: Response containing all provider types with 'services', 'voices',
                'total_services', and 'total_voices' keys.
        """
        response = self.client.get("providers/all")
        return response['json']

    def get_voice(self, voice_id):
        """
        Get detailed information about a specific voice.

        Args:
            voice_id (int): ID of the voice to retrieve.

        Returns:
            dict: Response containing the voice details.
        """
        if not isinstance(voice_id, int) or voice_id < 1:
            raise ValueError("voice_id must be a positive integer")

        try:
            response = self.client.get(f"providers/voice/{voice_id}")
            return response['json']
        except APIError as e:
            # handle rate limiting 
            if e.status_code == 429:
                retry_after = getattr(e, 'response', {}).get('retry_after', 60)
                raise ValueError(f"Rate limit exceeded. Please wait {retry_after} seconds before trying again.")
            # handle authentication errors
            elif e.status_code == 401:
                raise ValueError("Authentication failed. Please check your API key.")
            # handle not found errors
            elif e.status_code == 404:
                raise ValueError(f"Voice with ID {voice_id} was not found.")
            # let other API errors fill up with backend's message
            else:
                raise ValueError(f"API Error: {e.message}")
