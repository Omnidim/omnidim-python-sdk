import os
import base64
import json
from omnidimension import Client

# Initialize the OmniDimension client
api_key = os.environ.get('OMNIDIM_API_KEY', 'YBNmK6VxNLnPkIxwRNbZBKFR5C6_sRP0sSUFZeMr4p8')
# production 
client = Client(api_key)
# staging
client = Client(api_key, base_url='https://dashboard.staging.omnidim.io/api/v1/')

# ===== Example Usage Functions =====

def run_agent_examples():
    """Run examples for agent operations"""
    print("\n===== RUNNING AGENT EXAMPLES =====\n")
    
    # List agents
    agents_data = list_agents()
    
    # Create a basic agent
    agent_data = create_agent_with_full_config(
        name="Example Agent",
        welcome_message="Hello! I'm an example agent created using the OmniDimension SDK.",
        context_breakdown=[
            {"title": "Purpose", "body": "This agent demonstrates the SDK capabilities."}
        ],
        post_call_actions={
            "email": {
                "enabled": True,
                "recipients": ["example@example.com"],
                "include": ["summary", "extracted_variables"]
            },
            "extracted_variables": [
                {
                    "key": "caller_product_interest",
                    "prompt": "Identify the products the caller is interested in..."
                },
            ]
        }
    )
    
    # Get the agent ID
    agent_id = agent_data.get('id')
    if agent_id:
        # Get agent details
        get_agent(agent_id)
        
        # Update the agent
        update_agent(agent_id, {"name": "Updated Example Agent"})
        
        # Uncomment to delete the agent
        # delete_agent(agent_id)

def run_call_log_examples():
    """Run examples for call log operations"""
    print("\n===== RUNNING CALL LOG EXAMPLES =====\n")
    
    # Get call logs
    call_logs = get_call_logs()
    
    # Example: Get call logs filtered by status (uncomment to use)
    # call_logs_filtered = get_call_logs(call_status="completed")
    # call_logs_by_agent = get_call_logs(agent_id=123)
    
    # Get details of the first call log if available
    if call_logs.get('call_log_data') and len(call_logs['call_log_data']) > 0:
        call_log_id = call_logs['call_log_data'][0]['id']
        get_call_log_details(call_log_id)
    else:
        print("No call logs found.")
    
    # Uncomment to dispatch a call
    # agents_data = list_agents()
    # if agents_data.get('bots') and len(agents_data['bots']) > 0:
    #     agent_id = agents_data['bots'][0]['id']
    #     dispatch_call(agent_id, '+1234567890')

def run_integration_examples():
    """Run examples for integration operations"""
    print("\n===== RUNNING INTEGRATION EXAMPLES =====\n")
    
    # Get integration format examples
    get_integration_format_examples()
    
    # Get user integrations
    get_user_integrations()
    
    # Create a custom API integration
    api_integration = create_custom_api_integration(
        name="Weather API Integration",
        description="Integration with weather service",
        url="https://api.weatherapi.com/v1/current.json",
        method="GET",
        headers=[
            {"key": "Content-Type", "value": "application/json"}
        ],
        query_params=[
            
            {
                "key": "q",
                "description": "Location query",
                "type": "string",
                "required": True,
                "isLLMGenerated": True
            }
        ]
    )
    
    # Create a Cal.com integration
    cal_integration = create_cal_integration(
        name="Meeting Scheduler Integration",
        description="Integration with Cal.com calendar",
        cal_api_key="cal_api_key_example",
        cal_id="cal_user_id_example",
        cal_timezone="America/New_York"
    )
    
    # Create integration from JSON
    integration_data = {
        "name": "CRM API Integration",
        "description": "Integration with CRM service",
        "url": "https://api.crm-example.com/v1/contacts",
        "method": "POST",
        "integration_type": "custom_api",
        "headers": [
            {"key": "Authorization", "value": "Bearer token123"},
            {"key": "Content-Type", "value": "application/json"}
        ],
        "body_type": "json",
        "body_params": [
            {
                "key": "name",
                "description": "Contact name",
                "type": "string",
                "required": True,
                "isLLMGenerated": True
            },
            {
                "key": "email",
                "description": "Contact email",
                "type": "string",
                "required": True,
                "isLLMGenerated": True
            },
            {
                "key": "phone",
                "description": "Contact phone number",
                "type": "string",
                "required": False,
                "isLLMGenerated": True
            }
        ]
    }
    json_integration = create_integration_from_json(integration_data)
    
    # Create an agent for integration examples
    agent_data = create_agent(
        name="Integration Test Agent",
        welcome_message="Hello! I'm an agent for testing integrations.",
        context_breakdown=[
            {"title": "Purpose", "body": "This agent demonstrates integration capabilities."}
        ]
    )
    
    # Get the agent ID and integration ID
    agent_id = agent_data.get('id')
    api_integration_id = api_integration.get('id')
    
    if agent_id and api_integration_id:
        # Add integration to agent
        add_integration_to_agent(agent_id, api_integration_id)
        
        # Get agent integrations
        get_agent_integrations(agent_id)
        
        # Remove integration from agent
        remove_integration_from_agent(agent_id, api_integration_id)

def run_knowledge_base_examples():
    """Run examples for knowledge base operations"""
    print("\n===== RUNNING KNOWLEDGE BASE EXAMPLES =====\n")
    
    # List all knowledge base files
    list_knowledge_base_files()
    
    # Check if a file can be uploaded (1MB file)
    check_file_upload_capability(1024 * 1024)
    
    # Get an agent ID for attaching files
    agents_data = list_agents()
    agent_id = agents_data.get('bots', [{}])[0].get('id') if agents_data.get('bots') and len(agents_data['bots']) > 0 else None
    
    # Upload a file if sample.pdf exists
    try:
        file_data = upload_file_to_knowledge_base("sample.pdf")
        file_id = file_data.get('file', {}).get('id')
        
        if file_id and agent_id:
            # Attach file to agent
            attach_files_to_agent([file_id], agent_id)
            
            # Detach file from agent
            detach_files_from_agent([file_id], agent_id)
            
            # Delete file from knowledge base
            delete_file_from_knowledge_base(file_id)
    except FileNotFoundError:
        print("sample.pdf not found. Skipping file upload examples.")

def run_phone_number_examples():
    """Run examples for phone number operations"""
    print("\n===== RUNNING PHONE NUMBER EXAMPLES =====\n")
    
    # List all phone numbers
    phone_numbers = list_phone_numbers()
    
    # Get an agent ID
    agents_data = list_agents()
    agent_id = agents_data.get('bots', [{}])[0].get('id') if agents_data.get('bots') and len(agents_data['bots']) > 0 else None
    
    # Get the first phone number ID if available
    phone_number_id = None
    if phone_numbers.get('phone_numbers') and len(phone_numbers['phone_numbers']) > 0:
        phone_number_id = phone_numbers['phone_numbers'][0]['id']
    
    if phone_number_id and agent_id:
        # Attach phone number to agent
        attach_phone_number_to_agent(phone_number_id, agent_id)
        
        # Detach phone number
        detach_phone_number(phone_number_id)


# Helper function to pretty print JSON responses
def print_json_response(response, title=None):
    """Pretty print JSON responses"""
    if title:
        print(f"\n=== {title} ===\n")

    if isinstance(response, dict):
        # print status if available
        status = response.get('status')
        if status:
            print(f"Status: {status}")

        # handle direct JSON response structure
        if 'json' in response:
            # Old nested structure
            json_data = response.get('json')
            if json_data:
                print(json.dumps(json_data, indent=2))
            else:
                print(json.dumps(response, indent=2))
        else:
            # direct structure
            print(json.dumps(response, indent=2))
    else:
        print(json.dumps(response, indent=2))

    return response

# ===== Agent Operations =====

def list_agents(page=1, page_size=10):
    """List all agents with pagination"""
    response = client.agent.list(page=page, page_size=page_size)
    return print_json_response(response, "Listing all agents")

def create_agent(name, welcome_message, context_breakdown):
    """Create a new agent with basic configuration"""
    response = client.agent.create(
        name=name,
        welcome_message=welcome_message,
        context_breakdown=context_breakdown
    )
    return print_json_response(response, f"Creating agent: {name}")

def create_agent_with_full_config(name, welcome_message, context_breakdown, transcriber=None, model=None, 
                                voice=None, web_search=None, post_call_actions=None, filler=None):
    """Create a new agent with full configuration options"""
    # Set default configurations if not provided
    if transcriber is None:
        transcriber = {
            "provider": "deepgram_stream",
            "silence_timeout_ms": 400
        }
    
    if model is None:
        model = {
            "model": "gpt-4o-mini",
            "temperature": 0.7
        }
    
    if voice is None:
        voice = {
            "provider": "eleven_labs",
            "voice_id": "JBFqnCBsd6RMkjVDRZzb"
        }
    
    if web_search is None:
        web_search = {
            "enabled": True,
            "provider": "DuckDuckGo"
        }
    
    if filler is None:
        filler = {
            "enabled": True,
            "after_sec": 0,
            "fillers": ['let me check'],
        }
    
    response = client.agent.create(
        name=name,
        welcome_message=welcome_message,
        context_breakdown=context_breakdown,
        transcriber=transcriber,
        model=model,
        voice=voice,
        web_search=web_search,
        post_call_actions=post_call_actions,
        filler=filler
    )
    return print_json_response(response, f"Creating agent with full config: {name}")

def get_agent(agent_id):
    """Get details of a specific agent"""
    response = client.agent.get(agent_id)
    return print_json_response(response, f"Getting agent details (ID: {agent_id})")

def update_agent(agent_id, update_data):
    """Update an existing agent"""
    response = client.agent.update(agent_id, update_data)
    return print_json_response(response, f"Updating agent (ID: {agent_id})")

def delete_agent(agent_id):
    """Delete an agent"""
    response = client.agent.delete(agent_id)
    return print_json_response(response, f"Deleting agent (ID: {agent_id})")

# ===== Call Log Operations =====

def get_call_logs(page=1, page_size=10, agent_id=None, call_status=None):
    """Get all call logs with pagination and optional filtering"""
    response = client.call.get_call_logs(page=page, page_size=page_size, agent_id=agent_id, call_status=call_status)
    return print_json_response(response, "Getting call logs")

def get_call_log_details(call_log_id):
    """Get details of a specific call log"""
    response = client.call.get_call_log(call_log_id=call_log_id)
    return print_json_response(response, f"Getting call log details (ID: {call_log_id})")

def dispatch_call(agent_id, to_number):
    """Dispatch a call to a specific number using an agent"""
    response = client.call.dispatch_call(agent_id=agent_id, to_number=to_number)
    return print_json_response(response, f"Dispatching call to {to_number} using agent {agent_id}")

# ===== Integration Operations =====

def get_integration_format_examples():
    """Get examples of integration formats"""
    response = client.integrations.get_integration_format_examples()
    return print_json_response(response, "Getting integration format examples")

def get_user_integrations():
    """Get all integrations for the current user"""
    response = client.integrations.get_user_integrations()
    return print_json_response(response, "Getting user integrations")

def create_custom_api_integration(name, description, url, method, headers=None, query_params=None, body_params=None):
    """Create a custom API integration"""
    response = client.integrations.create_custom_api_integration(
        name=name,
        description=description,
        url=url,
        method=method,
        headers=headers or [],
        query_params=query_params or [],
        body_params=body_params or []
    )
    return print_json_response(response, f"Creating custom API integration: {name}")

def create_cal_integration(name, description, cal_api_key, cal_id, cal_timezone):
    """Create a Cal.com integration"""
    response = client.integrations.create_cal_integration(
        name=name,
        description=description,
        cal_api_key=cal_api_key,
        cal_id=cal_id,
        cal_timezone=cal_timezone
    )
    return print_json_response(response, f"Creating Cal.com integration: {name}")

def create_integration_from_json(integration_data):
    """Create an integration from a JSON configuration"""
    response = client.integrations.create_integration_from_json(integration_data)
    return print_json_response(response, f"Creating integration from JSON: {integration_data.get('name')}")

def add_integration_to_agent(agent_id, integration_id):
    """Add an integration to an agent"""
    response = client.integrations.add_integration_to_agent(
        agent_id=agent_id,
        integration_id=integration_id
    )
    return print_json_response(response, f"Adding integration (ID: {integration_id}) to agent (ID: {agent_id})")

def get_agent_integrations(agent_id):
    """Get all integrations for a specific agent"""
    response = client.integrations.get_agent_integrations(agent_id)
    return print_json_response(response, f"Getting integrations for agent (ID: {agent_id})")

def remove_integration_from_agent(agent_id, integration_id):
    """Remove an integration from an agent"""
    response = client.integrations.remove_integration_from_agent(
        agent_id=agent_id,
        integration_id=integration_id
    )
    return print_json_response(response, f"Removing integration (ID: {integration_id}) from agent (ID: {agent_id})")

# ===== Knowledge Base Operations =====

def list_knowledge_base_files():
    """List all knowledge base files"""
    response = client.knowledge_base.list()
    return print_json_response(response, "Listing all knowledge base files")

def check_file_upload_capability(file_size):
    """Check if a file of the given size can be uploaded"""
    response = client.knowledge_base.can_upload(file_size)
    return print_json_response(response, f"Checking if a file of size {file_size} bytes can be uploaded")

def upload_file_to_knowledge_base(file_path, file_name=None):
    """Upload a file to the knowledge base"""
    if file_name is None:
        file_name = os.path.basename(file_path)
    
    with open(file_path, "rb") as file:
        file_data = base64.b64encode(file.read()).decode('utf-8')
    
    response = client.knowledge_base.create(file_data, file_name)
    return print_json_response(response, f"Uploading file: {file_name}")

def attach_files_to_agent(file_ids, agent_id):
    """Attach files to an agent"""
    response = client.knowledge_base.attach(file_ids, agent_id)
    return print_json_response(response, f"Attaching files to agent (ID: {agent_id})")

def detach_files_from_agent(file_ids, agent_id):
    """Detach files from an agent"""
    response = client.knowledge_base.detach(file_ids, agent_id)
    return print_json_response(response, f"Detaching files from agent (ID: {agent_id})")

def delete_file_from_knowledge_base(file_id):
    """Delete a file from the knowledge base"""
    response = client.knowledge_base.delete(file_id)
    return print_json_response(response, f"Deleting file from knowledge base (ID: {file_id})")

# ===== Phone Number Operations =====

def list_phone_numbers(page=1, page_size=10):
    """List all phone numbers with pagination"""
    response = client.phone_number.list(page=page, page_size=page_size)
    return print_json_response(response, "Listing all phone numbers")

def attach_phone_number_to_agent(phone_number_id, agent_id):
    """Attach a phone number to an agent"""
    response = client.phone_number.attach(phone_number_id, agent_id)
    return print_json_response(response, f"Attaching phone number (ID: {phone_number_id}) to agent (ID: {agent_id})")

def detach_phone_number(phone_number_id):
    """Detach a phone number from its associated agent"""
    response = client.phone_number.detach(phone_number_id)
    return print_json_response(response, f"Detaching phone number (ID: {phone_number_id})")

# ===== Bulk Call Operations =====

def run_bulk_call_examples():
    """Run examples for bulk call operations"""
    print("\n===== RUNNING BULK CALL EXAMPLES =====\n")
    
    # Fetch all bulk calls
    bulk_calls = fetch_bulk_calls()
    
    # Get phone number ID for bulk calls
    phone_numbers = list_phone_numbers()
    phone_number_id = None
    if phone_numbers.get('phone_numbers') and len(phone_numbers['phone_numbers']) > 0:
        phone_number_id = phone_numbers['phone_numbers'][0]['id']
        print(f"Using phone number ID: {phone_number_id}")
    else:
        print("No phone numbers found. Please add a phone number first.")
        return
    
    # Create a bulk call campaign
    contact_list = [
        {
            "phone_number": "+1234567890",
            "customer_name": "John Doe",
            "product_interest": "Premium Plan"
        },
        {
            "phone_number": "+1987654321", 
            "customer_name": "Jane Smith",
            "product_interest": "Basic Plan"
        }
    ]
    
    # Create immediate bulk call
    bulk_call_data = create_bulk_calls(
        name="Marketing Campaign - Q4 2024",
        contact_list=contact_list,
        phone_number_id=phone_number_id
    )
    
    bulk_call_id = bulk_call_data.get('id')
    
    if bulk_call_id:
        # Get bulk call details
        get_bulk_call_details(bulk_call_id)
        
        # Pause the bulk call
        pause_bulk_call(bulk_call_id)
        
        # Resume the bulk call
        resume_bulk_call(bulk_call_id)
        
        # Reschedule the bulk call
        reschedule_bulk_call(bulk_call_id, "2024-12-25 10:00:00", "America/New_York")
        
        # Cancel the bulk call
        cancel_bulk_call(bulk_call_id)
    
    # Create a scheduled bulk call
    scheduled_bulk_call = create_scheduled_bulk_calls(
        name="Scheduled Campaign - New Year",
        contact_list=contact_list,
        phone_number_id=phone_number_id,
        scheduled_datetime="2024-12-31 09:00:00",
        timezone="America/New_York"
    )

def fetch_bulk_calls(page=1, page_size=10, status=None):
    """Fetch all bulk calls with optional filtering and pagination"""
    response = client.bulk_call.fetch_bulk_calls(page=page, page_size=page_size, status=status)
    return print_json_response(response, "Fetching bulk calls")

def create_bulk_calls(name, contact_list, phone_number_id, is_scheduled=False, scheduled_datetime=None, timezone='UTC'):
    """Create a new bulk call campaign"""
    response = client.bulk_call.create_bulk_calls(
        name=name,
        contact_list=contact_list,
        phone_number_id=phone_number_id,
        is_scheduled=is_scheduled,
        scheduled_datetime=scheduled_datetime,
        timezone=timezone
    )
    return print_json_response(response, f"Creating bulk call: {name}")

def create_scheduled_bulk_calls(name, contact_list, phone_number_id, scheduled_datetime, timezone='UTC'):
    """Create a scheduled bulk call campaign"""
    response = client.bulk_call.create_bulk_calls(
        name=name,
        contact_list=contact_list,
        phone_number_id=phone_number_id,
        is_scheduled=True,
        scheduled_datetime=scheduled_datetime,
        timezone=timezone
    )
    return print_json_response(response, f"Creating scheduled bulk call: {name}")

def get_bulk_call_details(bulk_call_id):
    """Get detailed information about a specific bulk call campaign"""
    response = client.bulk_call.detail_bulk_calls(bulk_call_id)
    return print_json_response(response, f"Getting bulk call details (ID: {bulk_call_id})")

def pause_bulk_call(bulk_call_id):
    """Pause a bulk call campaign"""
    response = client.bulk_call.bulk_calls_actions(bulk_call_id, 'pause')
    return print_json_response(response, f"Pausing bulk call (ID: {bulk_call_id})")

def resume_bulk_call(bulk_call_id):
    """Resume a bulk call campaign"""
    response = client.bulk_call.bulk_calls_actions(bulk_call_id, 'resume')
    return print_json_response(response, f"Resuming bulk call (ID: {bulk_call_id})")

def reschedule_bulk_call(bulk_call_id, new_scheduled_datetime, new_timezone=None):
    """Reschedule a bulk call campaign"""
    response = client.bulk_call.bulk_calls_actions(
        bulk_call_id, 
        'reschedule', 
        new_timezone=new_timezone,
        new_scheduled_datetime=new_scheduled_datetime
    )
    return print_json_response(response, f"Rescheduling bulk call (ID: {bulk_call_id})")

def cancel_bulk_call(bulk_call_id):
    """Cancel a bulk call campaign"""
    response = client.bulk_call.cancel_bulk_calls(bulk_call_id)
    return print_json_response(response, f"Cancelling bulk call (ID: {bulk_call_id})")

# ===== Providers Operations =====



def run_providers_examples():
    """run examples for providers operations"""
    print("\n===== RUNNING PROVIDERS EXAMPLES =====\n")

    # List all LLM providers
    list_all_llms()

    # List all voice providers with pagination
    list_all_voices()

    # List all STT providers
    list_all_stt()

    # List all TTS providers
    list_all_tts()

    # List all providers (comprehensive)
    list_all_providers()

    # Search ElevenLabs voices with filters
    search_elevenlabs_voices()

    # Filter voices by criteria
    filter_voices_by_criteria()

    # Get voice details
    get_specific_voice_details()

    # Test pagination and iteration
    test_pagination_iteration()

    # Test error handling
    test_error_handling_examples()
    
    
    
def list_all_llms():
    """List all available LLM providers"""
    response = client.providers.list_llms()
    return print_json_response(response, "Listing all LLM providers")

def list_all_voices(page=1, page_size=30):
    """List all available voice providers with pagination"""
    response = client.providers.list_voices(page=page, page_size=page_size)
    return print_json_response(response, f"Listing all voices (page {page}, size {page_size})")

def list_all_stt():
    """List all available STT providers"""
    response = client.providers.list_stt()
    return print_json_response(response, "Listing all STT providers")

def list_all_tts():
    """List all available TTS providers"""
    response = client.providers.list_tts()
    return print_json_response(response, "Listing all TTS providers")

def list_all_providers():
    """List all providers (comprehensive)"""
    response = client.providers.list_all()
    return print_json_response(response, "Listing all providers (comprehensive)")

def search_elevenlabs_voices():
    """Search ElevenLabs voices with various filters"""
    print("\n--- Searching ElevenLabs voices by search term ---")
    response = client.providers.list_voices(provider='eleven_labs', search='excited', gender='male', page_size=10)
    print_json_response(response, "ElevenLabs excited male voices")

    print("\n--- Searching ElevenLabs voices by language ---")
    response = client.providers.list_voices(provider='eleven_labs', language='en', page_size=10)
    print_json_response(response, "ElevenLabs English voices")

    print("\n--- Searching ElevenLabs voices by accent ---")
    response = client.providers.list_voices(provider='eleven_labs', accent='american', gender='female', page_size=10)
    print_json_response(response, "ElevenLabs American female voices")

def filter_voices_by_criteria():
    """Demonstrate various voice filtering options"""
    print("\n--- Filtering voices by provider ---")
    response = client.providers.list_voices(provider='eleven_labs', page_size=20)
    print_json_response(response, "ElevenLabs voices only")

    print("\n--- Combined filters ---")
    response = client.providers.list_voices(
        provider='eleven_labs',
        search='professional',
        language='en',
        accent='british',
        gender='male',
        page_size=15
    )
    print_json_response(response, "ElevenLabs professional British male voices")

def get_specific_voice_details():
    """Get details of a specific voice"""
    # first get some voices to pick an ID from
    
    voices_response = client.providers.list_voices(page_size=5)
    if voices_response.get('voices') and len(voices_response['voices']) > 0:
        voice_id = voices_response['voices'][0]['id']
        print(f"\n--- Getting details for voice ID: {voice_id} ---")
        response = client.providers.get_voice(voice_id)
        print_json_response(response, f"Voice details for ID {voice_id}")
    else:
        print("No voices found to get details for.")

def test_pagination_iteration():
    """test pagination and iteration"""
    print("\n--- Testing pagination and iteration ---")

    print("\n--- Manual pagination ---")
    page = 1
    total_voices = 0
    while total_voices < 10 and page <= 3:  # limit to 3 pages for demo
        response = client.providers.list_voices(page=page, page_size=3)
        voices = response.get('voices', [])
        print(f"Page {page}: {len(voices)} voices")
        total_voices += len(voices)
        page += 1

    print(f"\n--- Total voices retrieved: {total_voices} ---")

def test_error_handling_examples():
    """test error handling and edge cases"""
    print("\n--- Testing error handling ---")

    print("\n--- Testing invalid parameters ---")
    try:
        client.providers.list_voices(page=0)
    except ValueError as e:
        print(f"[ERROR] Invalid page handled: {e}")

    try:
        client.providers.list_voices(page_size=150)
    except ValueError as e:
        print(f"[ERROR] Invalid page_size handled: {e}")

    try:
        client.providers.list_voices(provider='eleven_labs', gender='invalid')
    except ValueError as e:
        print(f"[ERROR] Invalid gender handled: {e}")

    print("\n--- Testing unsupported filters on non-ElevenLabs provider ---")
    try:
        client.providers.list_voices(provider='google', search='test')
    except ValueError as e:
        print(f"[ERROR] Unsupported filter handled: {e}")

    print("\n--- Testing rate limiting ---")
    try:
        # make several rapid requests to potentially trigger rate limiting
        for i in range(5):
            response = client.providers.list_voices(provider='eleven_labs', page_size=1)
            print(f"[INFO] Request {i+1}: Success")
    except ValueError as e:
        if 'Rate limit exceeded' in str(e):
            print(f"[INFO] Rate limiting working: {e}")
        else:
            print(f"[ERROR] Unexpected error: {e}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")


if __name__ == "__main__":
    # Uncomment the function you want to run
    # run_agent_examples()
    # run_call_log_examples()
    # run_integration_examples()
    # run_knowledge_base_examples()
    # run_phone_number_examples()
    # run_bulk_call_examples()
    run_providers_examples()

