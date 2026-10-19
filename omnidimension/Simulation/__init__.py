class Simulation():
    def __init__(self, client):
        """
        Initialize the Simulation client with a reference to the main API client.
        
        Args:
            client: The main API client instance.
        """
        self.client = client

    def create(self, name, agent_id, number_of_call_to_make=1, concurrent_call_count=3, 
               max_call_duration_in_minutes=3, scenarios=None):
        """
        Create a new simulation with specified scenarios to test your agent's performance.

        Args:
            name (str): Name of the simulation for identification.
            agent_id (int): ID of the agent to test.
            number_of_call_to_make (int, optional): Number of calls to make per scenario (default: 1).
            concurrent_call_count (int, optional): Number of concurrent calls to run (default: 3).
            max_call_duration_in_minutes (int, optional): Maximum duration for each call in minutes (default: 3).
            scenarios (list, optional): List of test scenarios to execute.

        Returns:
            dict: Response from the API containing success status and simulation details.

        Raises:
            ValueError: If required fields are missing or invalid.

        Example:
            ```python
            # Create a simulation with scenarios
            client.simulation.create(
                name="Restaurant Order Taking Test",
                agent_id=123,
                number_of_call_to_make=1,
                concurrent_call_count=3,
                max_call_duration_in_minutes=3,
                scenarios=[
                    {
                        "name": "Order Pizza",
                        "description": "1. Act as a customer wanting to order pizza\\n2. Ask for menu items\\n3. Order a large pepperoni pizza\\n4. Provide contact details\\n5. End call with thank you",
                        "expected_result": "Order should be placed successfully and confirmation provided",
                        "selected_voices": [
                            {"id": "voice_id_1", "provider": "eleven_labs"},
                            {"id": "voice_id_2", "provider": "play_ht"}
                        ]
                    }
                ]
            )
            ```
        """
        # Validate required inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string.")
        
        if not isinstance(agent_id, int):
            raise ValueError("Agent ID must be an integer.")

        # Validate scenarios if provided
        if scenarios is not None:
            self._validate_scenarios(scenarios)

        data = {
            "name": name,
            "agent_id": agent_id,
            "number_of_call_to_make": number_of_call_to_make,
            "concurrent_call_count": concurrent_call_count,
            "max_call_duration_in_minutes": max_call_duration_in_minutes
        }

        if scenarios is not None:
            data["scenarios"] = scenarios

        return self.client.post("simulations", data=data)

    def list(self, pageno=1, pagesize=10):
        """
        Retrieve all simulations for the authenticated user with pagination support.

        Args:
            pageno (int, optional): Page number for pagination (default: 1).
            pagesize (int, optional): Number of records per page (default: 10).

        Returns:
            dict: Response containing the list of simulations.

        Example:
            ```python
            # List all simulations with pagination
            response = client.simulation.list(pageno=1, pagesize=10)
            ```
        """
        params = {
            'pageno': pageno,
            'pagesize': pagesize
        }
        return self.client.get("simulations", params=params)

    def get(self, simulation_id):
        """
        Retrieve detailed information about a specific simulation including status, progress, and results.

        Args:
            simulation_id (int): The ID of the simulation to retrieve.

        Returns:
            dict: Response containing the simulation details.

        Raises:
            ValueError: If simulation_id is not an integer.

        Example:
            ```python
            # Get details of a specific simulation
            simulation_id = 456
            response = client.simulation.get(simulation_id)
            ```
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")

        return self.client.get(f"simulations/{simulation_id}")

    def update(self, simulation_id, data):
        """
        Update an existing simulation. Cannot update simulations that are currently in progress.

        Args:
            simulation_id (int): The ID of the simulation to update.
            data (dict): Dictionary containing the fields to update. Can include any field from create simulation.

        Returns:
            dict: Response from the API containing success status and updated simulation details.

        Raises:
            ValueError: If required fields are missing or invalid.

        Example:
            ```python
            # Update an existing simulation
            simulation_id = 456
            update_data = {
                "name": "Updated Restaurant Test",
                "max_call_duration_in_minutes": 5,
                "scenarios": [
                    {
                        "name": "Updated Order Pizza",
                        "description": "Updated instructions...",
                        "expected_result": "Updated expected behavior..."
                    }
                ]
            }
            response = client.simulation.update(simulation_id, update_data)
            ```
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")
        
        if not isinstance(data, dict) or not data:
            raise ValueError("Update data must be a non-empty dictionary.")

        # Validate scenarios if provided in update data
        if "scenarios" in data and data["scenarios"] is not None:
            self._validate_scenarios(data["scenarios"])

        return self.client.put(f"simulations/{simulation_id}", data=data)

    def delete(self, simulation_id):
        """
        Delete (deactivate) a simulation. Running simulations are automatically stopped first.

        Args:
            simulation_id (int): The ID of the simulation to delete.

        Returns:
            dict: Response from the API containing success status.

        Raises:
            ValueError: If simulation_id is not an integer.

        Example:
            ```python
            # Delete a simulation
            simulation_id = 456
            response = client.simulation.delete(simulation_id)
            ```
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")

        return self.client.delete(f"simulations/{simulation_id}")

    def start(self, simulation_id):
        """
        Start a simulation. You can optionally update scenarios before starting the test run.

        Args:
            simulation_id (int): The ID of the simulation to start.
            scenarios (list, optional): Optional array of scenarios to update before starting.

        Returns:
            dict: Response from the API containing success status and simulation start details.

        Raises:
            ValueError: If simulation_id is not an integer or scenarios format is invalid.

        Example:
            ```python
            # Start a simulation
            simulation_id = 456
            response = client.simulation.start(simulation_id)

            # Start with updated scenarios
            response = client.simulation.start(
                simulation_id,
            )
            ```
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")

        return self.client.post(f"simulations/{simulation_id}/start", data={})

    def stop(self, simulation_id):
        """
        Stop a running simulation and disconnect any ongoing test calls.

        Args:
            simulation_id (int): The ID of the simulation to stop.

        Returns:
            dict: Response from the API containing success status.

        Raises:
            ValueError: If simulation_id is not an integer.

        Example:
            ```python
            # Stop a running simulation
            simulation_id = 456
            response = client.simulation.stop(simulation_id)
            ```
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")

        return self.client.post(f"simulations/{simulation_id}/stop")

    def enhance_prompt(self, simulation_id):
        """
        Analyze a completed simulation and receive AI-powered suggestions for improving your agent's prompts and performance.

        Args:
            simulation_id (int): The ID of the completed simulation to analyze.

        Returns:
            dict: Response containing enhanced prompt suggestions.

        Raises:
            ValueError: If simulation_id is not an integer.

        Example:
            ```python
            # Get enhanced prompt suggestions
            simulation_id = 456
            response = client.simulation.enhance_prompt(simulation_id)
            ```
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")

        return self.client.post(f"simulations/{simulation_id}/enhance-prompt")

    def apply_enhanced_prompt(self, simulation_id):
        """
        Rewrite the agent's prompt sections from a completed simulation's
        suggestions. The agent's current sections are replaced.

        Args:
            simulation_id (int): The ID of the completed simulation.

        Returns:
            dict: Response containing the agent_id whose prompt changed.
        """
        if not isinstance(simulation_id, int):
            raise ValueError("Simulation ID must be an integer.")

        return self.client.post(f"simulations/{simulation_id}/apply-enhanced-prompt")

    def generate_scenarios(self, agent_id, number_of_scenarios):
        """
        Write test scenarios for an agent from its prompt. Nothing is saved:
        pass the ones you want to create().

        Args:
            agent_id (int): The ID of the agent.
            number_of_scenarios (int): How many scenarios to write.

        Returns:
            dict: Response containing the scenarios, each with name,
                description and expected_result.
        """
        return self.client.post(f"agents/{agent_id}/auto-scenarios",
                                data={"number_of_scenarios": number_of_scenarios})

    
    @staticmethod
    def _validate_scenarios(scenarios, allow_id=False):
        """
        Validate scenarios format.
        
        Args:
            scenarios: List of scenarios to validate.
            allow_id: Whether to allow 'id' field in scenarios (for updates).
            
        Raises:
            ValueError: If scenarios don't follow the expected format.
        """

        if not isinstance(scenarios, list):
            raise ValueError("Scenarios must be a list of dictionaries.")

        for scenario in scenarios:
            if not isinstance(scenario, dict):
                raise ValueError("Each scenario must be a dictionary.")

            # Check required fields
            required_fields = ['name', 'description', 'expected_result']
            for field in required_fields:
                if field not in scenario or not isinstance(scenario[field], str):
                    raise ValueError(f"Each scenario must contain a '{field}' field as a string.")

            # Validate selected_voices if provided
            if 'selected_voices' in scenario:
                voices = scenario['selected_voices']
                if not isinstance(voices, list):
                    raise ValueError("selected_voices must be a list of dictionaries.")
                
                for voice in voices:
                    if not isinstance(voice, dict):
                        raise ValueError("Each voice in selected_voices must be a dictionary.")
                    
                    if 'id' not in voice or 'provider' not in voice:
                        raise ValueError("Each voice must contain 'id' and 'provider' fields.")
                    
                    valid_providers = ['eleven_labs', 'deepgram', 'cartesia', 'rime', 'inworld']
                    if voice['provider'] not in valid_providers:
                        raise ValueError(f"Voice provider must be one of: {', '.join(valid_providers)}")
