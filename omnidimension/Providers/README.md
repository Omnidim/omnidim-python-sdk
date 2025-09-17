# Providers Module

The Providers module provides access to all AI service providers available in the OmniDimension platform, including LLMs, voices, STT, and TTS providers.

## Features

- **LLM Providers**: List all available Large Language Models (23 providers)
- **Voice Providers**: Advanced voice filtering with ElevenLabs support (104+ voices available through search)
- **STT Providers**: Speech-to-Text service providers (5 providers)
- **TTS Providers**: Text-to-Speech service providers (10 providers)
- **Comprehensive Listing**: Get all providers in a single request (38 services total)
- **Voice Details**: Get detailed information about specific voices
- **Advanced Filtering**: ElevenLabs-specific filters (search, language, accent, gender)
- **Pagination Support**: Handling of large result sets

## Quick Start

```python
from omnidimension import Client

client = Client('your-api-key')

# List all LLM providers
llms = client.providers.list_llms()
print(f"[SUCCESS] Found {llms['total']} LLM providers")

# List voices with pagination
voices = client.providers.list_voices(page=1, page_size=50)
print(f"[SUCCESS] Found {voices['total']} voices")

# Search ElevenLabs voices
professional_voices = client.providers.list_voices(
    provider='eleven_labs',
    search='professional',
    gender='male',
    page_size=20
)
```

## API Methods

### Core Methods

#### 1. `list_llms()`
Returns all available LLM providers.

```python
response = client.providers.list_llms()
# Response contains: {'llms': [...], 'total': 23}
```

**Response:**
```json
{
  "llms": [
    {
      "id": 11,
      "name": "gpt-4o",
      "display_name": "gpt-4o",
      "service_type": "LLM"
    },
    {
      "id": 12,
      "name": "gpt-4o-mini",
      "display_name": "gpt-4o-mini",
      "service_type": "LLM"
    }
  ],
  "total": 23
}
```

#### 2. `list_voices(provider=None, search=None, language=None, accent=None, gender=None, page=1, page_size=30)`
Returns voice providers with advanced filtering and pagination.

**Parameters:**
- `provider` (str): Filter by specific TTS provider ('eleven_labs', 'google', 'deepgram', 'cartesia', 'sarvam')
- `search` (str): Search term for voice name/description (ElevenLabs only)
- `language` (str): Language filter (ElevenLabs only, e.g., 'en', 'es', 'fr')
- `accent` (str): Accent filter (ElevenLabs only, e.g., 'american', 'british')
- `gender` (str): Gender filter ('male' or 'female', ElevenLabs only)
- `page` (int): Page number for pagination (default: 1)
- `page_size` (int): Number of items per page (default: 30, max: 100)

```python
# Get all voices
all_voices = client.providers.list_voices()

# Search ElevenLabs voices
professional_male = client.providers.list_voices(
    provider='eleven_labs',
    search='professional',
    gender='male',
    page_size=20
)

# Filter by language and accent
british_english = client.providers.list_voices(
    provider='eleven_labs',
    language='en',
    accent='british'
)
```

**Response:**
```json
{
  "voices": [
    {
      "id": 37,
      "name": "JBFqnCBsd6RMkjVDRZzb",
      "display_name": "George",
      "service": "eleven_labs",
      "sample_url": "https://storage.googleapis.com/eleven-public-prod/premade/voices/JBFqnCBsd6RMkjVDRZzb/e6206d1a-0721-4787-aafb-06a6e705cac5.mp3"
    },
    {
      "id": 1,
      "name": "aura-luna-en",
      "display_name": "luna",
      "service": "deepgram",
      "sample_url": "https://res.cloudinary.com/deepgram/video/upload/v1709565351/aura/luna_docs_clom0e.wav"
    }
  ],
  "total": 104,
  "page": 1,
  "page_size": 30
}
```

#### 3. `list_stt()`
Returns all available Speech-to-Text providers.

```python
stt_providers = client.providers.list_stt()
```

**Response:**
```json
{
  "stt": [
    {
      "id": 1,
      "name": "whisper",
      "display_name": "whisper",
      "service_type": "STT"
    },
    {
      "id": 2,
      "name": "deepgram_stream",
      "display_name": "deepgram_stream",
      "service_type": "STT"
    },
    {
      "id": 3,
      "name": "Cartesia",
      "display_name": "Cartesia",
      "service_type": "STT"
    },
    {
      "id": 4,
      "name": "Sarvam",
      "display_name": "Sarvam",
      "service_type": "STT"
    },
    {
      "id": 5,
      "name": "Azure",
      "display_name": "Azure",
      "service_type": "STT"
    }
  ],
  "total": 5
}
```

#### 4. `list_tts()`
Returns all available Text-to-Speech providers.

```python
tts_providers = client.providers.list_tts()
```

**Response:**
```json
{
  "tts": [
    {
      "id": 29,
      "name": "deepgram",
      "display_name": "deepgram",
      "service_type": "TTS"
    },
    {
      "id": 30,
      "name": "google",
      "display_name": "google",
      "service_type": "TTS"
    },
    {
      "id": 31,
      "name": "eleven_labs",
      "display_name": "eleven_labs",
      "service_type": "TTS"
    }
  ],
  "total": 10
}
```

#### 5. `list_all()`
Returns all providers (services and voices) in a comprehensive response.

```python
all_providers = client.providers.list_all()
```

**Response:**
```json
{
  "services": {
    "STT": [
      {
        "id": 1,
        "name": "whisper",
        "display_name": "whisper",
        "service_type": "STT"
      }
    ],
    "LLM": [
      {
        "id": 11,
        "name": "gpt-4o",
        "display_name": "gpt-4o",
        "service_type": "LLM"
      }
    ],
    "TTS": [
      {
        "id": 29,
        "name": "deepgram",
        "display_name": "deepgram",
        "service_type": "TTS"
      }
    ]
  },
  "voices": [
    {
      "id": 1,
      "name": "aura-luna-en",
      "display_name": "luna",
      "service": "deepgram",
      "sample_url": "https://res.cloudinary.com/deepgram/video/upload/v1709565351/aura/luna_docs_clom0e.wav"
    }
  ],
  "total_services": 38,
  "total_voices": 104
}
```

#### 6 .`get_voice(voice_id)`
Get detailed information about a specific voice.

```python
voice_info = client.providers.get_voice(1)
print(f"Voice: {voice_info['display_name']}")
```

**Response:**
```json
{
  "id": 1,
  "name": "aura-luna-en",
  "display_name": "luna",
  "service": "deepgram",
  "sample_url": "https://res.cloudinary.com/deepgram/video/upload/v1709565351/aura/luna_docs_clom0e.wav"
}
```

## Important Notes

### ElevenLabs Voice Coverage

**ElevenLabs Full Voice Library Access:**
- Our API provides access to ElevenLabs' complete voice library (1000+ voices)
- Use search, language, accent, and gender filters to find specific voices
- The API returns paginated results (up to 104 voices per page) but supports searching the entire ElevenLabs catalog
- All ElevenLabs voices are available through our search functionality

### Filter Support by Provider

**ElevenLabs (Premium Provider)**

- **FULL FILTER SUPPORT:**
    - `search` - Search by voice name/description
    - `language` - Filter by language (en, es, fr, etc.)
    - `accent` - Filter by accent (american, british, etc.)
    - `gender` - Filter by gender (male, female)

**All Other Providers (Deepgram, Google, Cartesia, Sarvam, etc.)**
[ERROR] **LIMITED FILTER SUPPORT:**
- `search`, `language`, `accent`, `gender` - **NOT SUPPORTED** (returns error response)
- `page` & `page_size` - **ONLY PAGINATION WORKS**

### Error Handling

The SDK provides user-friendly error messages for common issues:

```python
try:
    # This will work
    elevenlabs_voices = client.providers.list_voices(
        provider='eleven_labs',
        search='excited'
    )
except ValueError as e:
    print(f"Error: {e}")  # Rate limit exceeded. Please wait 60 seconds before trying again.

try:
    # This will return an error for non-ElevenLabs providers
    deepgram_voices = client.providers.list_voices(
        provider='deepgram',
        search='excited'  # Not supported
    )
except ValueError as e:
    print(f"Error: {e}")  # Advanced filtering (search, language, accent, gender) is only supported for provider 'eleven_labs'. Provider 'deepgram' only supports pagination.
```

### Pagination

- Default `page_size` is 30, maximum is 100
- Page numbering starts from 1
- All providers support pagination
- `total` field represents actual results returned

### Rate Limiting

- ElevenLabs requests are rate limited to 10 per minute per user/IP
- Caching is implemented to reduce API calls and improve performance
- Cached responses are served instantly for repeated requests

## Examples

### Basic Usage

```python
from omnidimension import Client

client = Client('your-api-key')

# Get all providers
llms = client.providers.list_llms()
voices = client.providers.list_voices()
stt = client.providers.list_stt()
tts = client.providers.list_tts()

print(f"[SUCCESS] LLMs: {llms['total']}, Voices: {voices['total']}, STT: {stt['total']}, TTS: {tts['total']}")
```

### Advanced Voice Filtering

```python
# Find professional male voices for ElevenLabs
professional_male = client.providers.list_voices(
    provider='eleven_labs',
    search='professional',
    gender='male',
    language='en',
    page_size=25
)

# Search by specific criteria
excited_voices = client.providers.list_voices(
    provider='eleven_labs',
    search='excited'
)

# Get voice details
if professional_male['voices']:
    voice_id = professional_male['voices'][0]['id']
    details = client.providers.get_voice(voice_id)
    print(f"[SUCCESS] Selected voice: {details['display_name']}")
```

### Working with Different Providers

```python
# ElevenLabs voices (full filtering support)
elevenlabs_voices = client.providers.list_voices(
    provider='eleven_labs',
    search='calm',
    gender='female',
    language='en'
)

# Google voices (pagination only)
google_voices = client.providers.list_voices(
    provider='google',
    page_size=50
)

# Deepgram voices (pagination only)
deepgram_voices = client.providers.list_voices(
    provider='deepgram',
    page=1,
    page_size=20
)
```

### Provider Overview

```python
# Get everything at once
all_providers = client.providers.list_all()

print(f"[SUCCESS] Total Services: {all_providers['total_services']}")
print(f"[SUCCESS] Total Voices: {all_providers['total_voices']}")

# Access specific service types
llm_providers = all_providers['services']['LLM']
tts_providers = all_providers['services']['TTS']
stt_providers = all_providers['services']['STT']
all_voices = all_providers['voices']
```

### Error Handling Examples

```python
# Parameter validation
try:
    client.providers.list_voices(page=0)
except ValueError as e:
    print(f"[ERROR] Invalid page: {e}")  # "page must be a positive integer (1 or greater)"

try:
    client.providers.list_voices(page_size=150)
except ValueError as e:
    print(f"[ERROR] Invalid page_size: {e}")  # "page_size must be an integer between 1 and 100"

try:
    client.providers.list_voices(gender='invalid')
except ValueError as e:
    print(f"[ERROR] Invalid gender: {e}")  # "gender must be 'male' or 'female'"

# Unsupported filters
try:
    client.providers.list_voices(
        provider='google',
        search='test'  # Not supported for Google
    )
except ValueError as e:
    print(f"[ERROR] Unsupported filter: {e}")  # "Advanced filtering (search, language, accent, gender) is only supported for provider 'eleven_labs'. Provider 'google' only supports pagination."

# Rate limiting
try:
    # Make many rapid requests
    for i in range(15):
        client.providers.list_voices(provider='eleven_labs', page_size=1)
except ValueError as e:
    print(f"[ERROR] Rate limited: {e}")  # "Rate limit exceeded. Please wait 60 seconds before trying again."

# Authentication errors
try:
    bad_client = Client('invalid-key')
    bad_client.providers.list_llms()
except Exception as e:
    print(f"[ERROR] Auth error: {e}")  # "API Error (401): Missing or invalid API key"

# Voice not found
try:
    client.providers.get_voice(999999)
except ValueError as e:
    print(f"[ERROR] Voice not found: {e}")  # "Voice with ID 999999 was not found."
```

## Tips # 

1. **Use Pagination**: Don't request all voices at once, use `page_size` appropriately
2. **Leverage Caching**: Repeated requests for the same filters will be served from cache
3. **Filter Efficiently**: Use specific filters to reduce result sets
4. **Choose Right Provider**: ElevenLabs for advanced filtering, others for basic listing
5. **Batch Operations**: Use `list_all()` when you need comprehensive data

## Troubleshooting

**Common Issues:**

1. **"Advanced filtering (search, language, accent, gender) is only supported for provider 'eleven_labs'. Provider 'X' only supports pagination."**: You're using search/language/accent/gender filters on non-ElevenLabs providers
2. **"Rate limit exceeded. Please wait 60 seconds before trying again."**: Wait before making more ElevenLabs requests
3. **"Voice with ID X was not found."**: The voice ID doesn't exist or is invalid
4. **"page must be a positive integer (1 or greater)"**: Page number must be >= 1
5. **"page_size must be an integer between 1 and 100"**: Page size is outside valid range
6. **"gender must be 'male' or 'female'"**: Gender parameter is invalid
7. **"API Error (401): Missing or invalid API key"**: Authentication failed

**Debug Tips:**

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check API key
print(f"[SUCCESS] API Key configured: {bool(client.api_key)}")

# Test basic connectivity
try:
    client.providers.list_llms()
    print("[SUCCESS] API connection successful")
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")

# Check response structure
response = client.providers.list_voices(page_size=1)
print(f"[SUCCESS] Response keys: {response.keys()}")
print(f"[SUCCESS] First voice: {response['voices'][0] if response['voices'] else 'No voices'}")
```

## Available Providers Summary

- **LLM Providers**: 23 (OpenAI, Anthropic, Google, Azure, etc.)
- **Voice Providers**: 104+ voices across 5 services (ElevenLabs: 1000+ via search, Deepgram, Google, Cartesia, Sarvam)
- **STT Providers**: 5 (Whisper, Deepgram, Cartesia, Sarvam, Azure)
- **TTS Providers**: 10 (Deepgram, Google, ElevenLabs, Cartesia, Hume, Inworld, OpenAI, Play.ht, Rime, Sarvam)

For the most up-to-date list, use the API methods above.
