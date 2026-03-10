
class Agent():
    def __init__(self, client):
        """
        Initialize the Agent client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client

    def list(self, page=1, page_size=30):
        """
        Get all agents for the authenticated user.
        
        Args:
            page (int): Page number for pagination (default: 1).
            page_size (int): Number of items per page (default: 30).
            
        Returns:
            dict: Response containing the list of agents.
        """
        params = {
            'pageno': page,
            'pagesize': page_size
        }
        return self.client.get("agents", params=params)
    
    def get(self, agent_id):
        """
        Get a specific agent by ID.
        
        Args:
            agent_id (int): The ID of the agent to retrieve.
            
        Returns:
            dict: Response containing the agent details.
        """
        return self.client.get(f"agents/{agent_id}")
    
    def create(self, name, context_breakdown, welcome_message=None, call_type=None,
               is_interruption_allowed=None, is_welcome_message_dynamic=None,
               is_welcome_message_interruption=None, transcriber=None, model=None,
               voice=None, web_search=None, post_call_actions=None, filler=None,
               background_track=None, voicemail=None, end_call=None, **kwargs):
        """
        Create a custom agent with the provided configuration and optional parameters.

        Args:
            name (str): Name for the agent.
            context_breakdown (list): List of context breakdowns, each containing:
                - title (str): Title of the section
                - body (str): Instructions/context for the section
                - is_enabled (bool): Whether this block is active
            welcome_message (str, optional): The initial message spoken by the agent.
            call_type (str, optional): 'Incoming' or 'Outgoing'.
            is_interruption_allowed (bool, optional): Allow user to interrupt the agent.
            is_welcome_message_dynamic (bool, optional): Generate dynamic welcome message.
            is_welcome_message_interruption (bool, optional): Allow interruption during welcome.
            transcriber (dict, optional): Transcriber configuration.
                - provider (str): 'whisper', 'deepgram_stream', 'Cartesia', 'Sarvam', 'Azure', 'Soniox'
                - silence_timeout_ms (int): Silence timeout in ms.
                - should_apply_noise_reduction (bool): Apply noise reduction.
            model (dict, optional): LLM configuration.
                - model (str): 'gpt-4o', 'gpt-4o-mini', 'claude-3-5-sonnet-latest', 'gemini-2.5-flash', etc.
                - temperature (float): LLM temperature.
            voice (dict, optional): Voice configuration.
                - provider (str): 'deepgram', 'google', 'eleven_labs', 'cartesia', 'playht', 'openAI', 'sarvam', etc.
                - voice_id (str): Provider-specific voice ID.
                - speech_speed (float): Speed multiplier.
            web_search (dict, optional): Web search configuration.
                - enabled (bool): Enable live web search.
                - provider (str): Default 'DuckDuckGo'.
            post_call_actions (dict, optional): Post call webhooks/emails.
                - email (dict): {'enabled': bool, 'recipients': list, 'include': ['summary', 'extracted_variables', 'fullConversation', 'sentiment'], 'extracted_variables': [{'key': str, 'prompt': str}]}
                - webhook (dict): {'enabled': bool, 'include': list}
            filler (dict, optional): Filler audio injection.
                - enabled (bool): Enable fillers (e.g. "hmm", "let me check").
                - after_sec (float): Seconds of silence before injecting filler.
            background_track (dict, optional): Ambient background noise/track configuration.
                - enabled (bool): Enable background track.
                - name (str): Track name.
                - volume (float): Volume level (default 0.2).
                - tts_volume_reduction (float): Ducking amount when TTS plays.
            voicemail (dict, optional): Voicemail detection configuration for outbound calls.
                - enabled (bool): Detect voicemail/answering machines.
                - message (str): Message to leave on voicemail.
            end_call (dict, optional): End call logic/messages configuration.
                - enabled (bool): Allow the agent to hang up proactively.
                - condition (str): Prompt condition for ending the call.
                - message (str): Final message to speak before hanging up.
            **kwargs: Additional optional parameters.

        Returns:
            dict: Response from the API containing agent details.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Validate required inputs
        if not isinstance(name, str):
            raise ValueError("name must be a string.")
        if not isinstance(context_breakdown, list) or not all(
            isinstance(context, dict) and 'title' in context and 'body' in context
            for context in context_breakdown
        ):
            raise ValueError(
                "context_breakdown must be a list of dictionaries with 'title' and 'body'."
            )

        # Prepare the data payload
        data = {
            "name": name,
            "context_breakdown": context_breakdown,
        }
        
        # Add explicitly defined optional parameters if they are provided
        if welcome_message is not None: data["welcome_message"] = welcome_message
        if call_type is not None: data["call_type"] = call_type
        if is_interruption_allowed is not None: data["is_interruption_allowed"] = is_interruption_allowed
        if is_welcome_message_dynamic is not None: data["is_welcome_message_dynamic"] = is_welcome_message_dynamic
        if is_welcome_message_interruption is not None: data["is_welcome_message_interruption"] = is_welcome_message_interruption
        if transcriber is not None: data["transcriber"] = transcriber
        if model is not None: data["model"] = model
        if voice is not None: data["voice"] = voice
        if web_search is not None: data["web_search"] = web_search
        if post_call_actions is not None: data["post_call_actions"] = post_call_actions
        if filler is not None: data["filler"] = filler
        if background_track is not None: data["background_track"] = background_track
        if voicemail is not None: data["voicemail"] = voicemail
        if end_call is not None: data["end_call"] = end_call
        
        # Include any additional kwargs
        data.update(kwargs)

        return self.client.post("agents/create", data=data)
    
    def update(self, agent_id, data):
        """
        Update an existing agent.
        
        Args:
            agent_id (int): The ID of the agent to update.
            data (dict): The updated agent data.
            
        Returns:
            dict: Response containing the updated agent details.
        """
        return self.client.put(f"agents/{agent_id}", data=data)
    
    def delete(self, agent_id):
        """
        Delete an agent.
        
        Args:
            agent_id (int): The ID of the agent to delete.
            
        Returns:
            dict: Response indicating success or failure.
        """
        return self.client.delete(f"agents/{agent_id}")
