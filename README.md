
# OmniDimension Python SDK

*Build and ship AI voice agents from a single prompt.*

OmniDimension lets you **build, test, and deploy** reliable voice AI assistants by simply describing them in plain text. The platform offers **rigorous simulation testing** and **real-time observability**, making it easy to debug and monitor agents in production.

👉 [Try the Web UI](https://www.omnidim.io/) — You can also build and test voice agents visually using our no-code interface.

---

## 🚀 Features

- **Prompt-based creation:** Define voice agents with natural language.
- **Drag-and-drop editor:** Chat or visually edit flows, voices, models, and more.
- **Prebuilt templates:** Use plug-and-play agent templates for common use cases.
- **Testing & monitoring:** Simulate edge cases and debug live calls.
- **Knowledge Base support:** Upload and attach documents (PDFs) for factual grounding.
- **Integrations:** Connect to external APIs, CRMs, or tools like Cal.com.
- **Phone agents:** Assign numbers and initiate real voice calls via the SDK.
- **Bulk Call:** Send multiple voice calls AI to multiple numbers simultaneously.

---

## 📦 Installation

### Basic SDK

```bash
pip install omnidimension
````

> Requires Python 3.9+

---

## 🔐 Authentication

First, obtain your API key from the OmniDimension dashboard. Store it in your environment variables:

### Linux/macOS

```bash
export OMNIDIM_API_KEY="your_api_key_here"
```

### Windows (CMD)

```cmd
set OMNIDIM_API_KEY=your_api_key_here
```

### In Python

```python
import os
from omnidimension import Client

api_key = os.environ.get("OMNIDIM_API_KEY")
client = Client(api_key)
```

---

## ✨ SDK Usage

```python
from omnidimension import Client

# Initialize the client with your API key
client = Client(api_key="your_api_key")

# List agents
agents = client.agent.list()
print(agents)
```

---

## 🛰️ MCP server

The OmniDimension MCP server lives in its own repositories, not in this SDK. Pick whichever fits your client.

### Hosted (no install)

Point any MCP client at the hosted server. It speaks the standard OAuth flow, so clients discover the rest automatically:

```
https://mcp.omnidim.io/mcp
```

For Claude Code:

```bash
claude mcp add --transport http omnidim https://mcp.omnidim.io/mcp --scope user
```

Source: [Omnidim/omnidim-mcp-cloud](https://github.com/Omnidim/omnidim-mcp-cloud)

### Local (stdio)

For clients that launch a local server (Claude Desktop, Cursor, Windsurf), use the npm package [`@omnidim-ai/mcp-server`](https://www.npmjs.com/package/@omnidim-ai/mcp-server). Save this as your MCP client config:

```json
{
  "mcpServers": {
    "omnidim": {
      "command": "npx",
      "args": ["-y", "@omnidim-ai/mcp-server"],
      "env": {
        "OMNIDIM_API_KEY": "<your_omnidim_api_key>"
      }
    }
  }
}
```

Source: [Omnidim/omnidim-mcp-server](https://github.com/Omnidim/omnidim-mcp-server)

---

##  📡 Providers API

The Providers API allows you to discover and explore all available AI providers for LLMs, voices, STT, and TTS services.

### Quick Examples

```python
# Get all LLM providers
llms = client.providers.list_llms()
print(f"[SUCCESS] Found {llms['total']} LLM providers")

# List voices with pagination
voices = client.providers.list_voices(page=1, page_size=50)
print(f"[SUCCESS] Found {voices['total']} voices")
```

> ![INFO]
> **[Complete Providers Documentation](omnidimension/Providers/README.md)**

---

## 📚 Knowledge Base

```python
files = client.knowledge_base.list()
print(files)

file_ids = [123]
agent_id = 456
response = client.knowledge_base.attach(file_ids, agent_id)
print(response)
```

---

## 🔌 Integrations

```python
response = client.integrations.create_custom_api_integration(
    name="WeatherAPI",
    url="https://api.example.com/weather",
    method="GET"
)
print(response)

client.integrations.add_integration_to_agent(agent_id=123, integration_id=789)
```

---

## ☎️ Phone Number Management

```python
numbers = client.phone_number.list(page=1, page_size=10)
print(numbers)

client.phone_number.attach(phone_number_id=321, agent_id=123)

# Search for numbers available to purchase in a region
available = client.phone_number.search(region="US", pattern="415", page=1, limit=20)
print(available)

# Purchase one of the numbers found above
purchase = client.phone_number.purchase(
    region="US",
    phone_number="+14155550123",
    idempotency_key="order-2024-12-01-001"  # safe to retry with the same key
)
print(purchase)

# Release a number you no longer need
client.phone_number.release(phone_number="+14155550123")
```

Reseller accounts can pass `user_id` to `list`, `search`, `purchase`, and `release` to act on a
specific child client's account instead of their own.

---

## 🤝 Reseller Management

Reseller-only methods for managing child organizations, users, credits, and KYC.

```python
# List child organizations
orgs = client.reseller.list_organizations()

# Create a new child user
new_user = client.reseller.add_user(
    name="Jane Doe",
    email="jane@example.com",
    phone="+14155550123",
    password="a-strong-password",
    welcome_minutes_to_credit=100,
    cost_per_min=0.05
)

# Control which dashboard menus a child user can see
client.reseller.set_access_control(
    user_id=456,
    dashboard_menu_access={"billing": True, "agents": True, "integrations": False}
)

# Set or clear a child account's expiry date
client.reseller.set_expiry(user_id=456, expiry_date="2025-12-31")
client.reseller.set_expiry(user_id=456)  # clears the expiry

# Set a child organization's concurrent call limit (absolute value, not a delta)
client.reseller.set_concurrency(child_organization_id=789, new_limit=10)

# Calculate and transfer credits
cost = client.reseller.calculate_credits(minutes=500, cost_per_min=0.05)
client.reseller.transfer_credits(to_organization_id=789, minutes=500, cost_per_min=0.05)

# Revert a previous transfer (uses the original rate, no cost_per_min to pass)
client.reseller.revert_credits(from_organization_id=789, minutes=500)

# Credit transfer/revert history
logs = client.reseller.credit_logs(page=1, page_size=30)

# KYC: check status, then walk next_step until it reports "completed"
status = client.reseller.kyc_status(user_id=456)
requirements = client.reseller.kyc_requirements(region="IN")
client.reseller.submit_kyc_step(step="register", user_id=456, region="IN", full_name="Jane Doe")
```

---

## 📞 Bulk Call Management

```python
# First, get your phone number IDs
phone_numbers = client.phone_number.list()
phone_number_id = phone_numbers['phone_numbers'][0]['id']  # Use the first available phone number

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
bulk_call = client.bulk_call.create_bulk_calls(
    name="Marketing Campaign - Q4 2024",
    contact_list=contact_list,
    phone_number_id=phone_number_id
)

# Create scheduled bulk call
scheduled_call = client.bulk_call.create_bulk_calls(
    name="Scheduled Campaign",
    contact_list=contact_list,
    phone_number_id=phone_number_id,
    is_scheduled=True,
    scheduled_datetime="2024-12-25 10:00:00",
    timezone="America/New_York"
)

# Create a draft campaign with number rotation and call conditions
draft = client.bulk_call.create_bulk_calls(
    name="Draft Campaign",
    contact_list=contact_list,
    phone_number_id=phone_number_id,
    save_as_draft=True,
    call_conditions=[
        {"column": "product_interest", "operator": "=", "value": "Premium Plan"}
    ],
    rotation={
        "numbers": [
            {"phone_number_id": phone_number_id, "sequence": 1},
            {"phone_number_id": 456, "sequence": 2}
        ],
        "strategy": "round_robin",
        "calls_per_number": 50
    },
    concurrent_call_limit=5
)
bulk_call_id = draft['json']['id']

# Add contacts to an existing campaign
client.bulk_call.add_contact(
    bulk_call_id=bulk_call_id,
    to_number="+1234567890",
    custom_variables={"customer_name": "John Doe"}
)
client.bulk_call.add_contacts(
    bulk_call_id=bulk_call_id,
    contacts=[
        {"to_number": "+1987654321", "custom_variables": {"customer_name": "Jane Smith"}}
    ]  # up to 1000 contacts per request
)

# Start the draft campaign
client.bulk_call.start_bulk_call(bulk_call_id=bulk_call_id)

# Fetch all bulk calls
bulk_calls = client.bulk_call.fetch_bulk_calls(page=1, page_size=10, status="active")

# Get bulk call details
details = client.bulk_call.detail_bulk_calls(bulk_call_id=123)

# Control bulk call actions
client.bulk_call.bulk_calls_actions(bulk_call_id=123, action="pause")
client.bulk_call.bulk_calls_actions(bulk_call_id=123, action="resume")
client.bulk_call.bulk_calls_actions(
    bulk_call_id=123, 
    action="reschedule",
    new_scheduled_datetime="2024-12-26 14:00:00",
    new_timezone="America/New_York"
)

# Cancel bulk call
client.bulk_call.cancel_bulk_calls(bulk_call_id=123)

# Live status of a running campaign
status = client.bulk_call.get_live_status(bulk_call_id=123)

# Call lines with cursor pagination and filters
lines = client.bulk_call.get_bulk_call_lines(
    bulk_call_id=123,
    pagesize=50,  # max 150
    call_status="completed",
    include_total=True
)
next_page = client.bulk_call.get_bulk_call_lines(
    bulk_call_id=123,
    cursor=lines['json']['next_cursor']
)

# Retry failed calls manually
client.bulk_call.manual_retry(bulk_call_id=123)

# Change the concurrent call limit of a campaign
client.bulk_call.update_concurrency(bulk_call_id=123, concurrent_call_limit=10)

# Manage the campaign's number rotation
numbers = client.bulk_call.list_rotation_numbers(bulk_call_id=123)
client.bulk_call.add_rotation_number(bulk_call_id=123, phone_number_id=456)
client.bulk_call.set_rotation_number_active(bulk_call_id=123, assignment_id=789, is_active=False)
```

---

## 📁 Recommended Project Structure

```
/docs/
  ├── agents/
  ├── calling/
  ├── integrations/
  ├── knowledge_base/
  └── phone_numbers/

/examples/         # Sample Python scripts
/cookbook/         # Ready-made project use cases
```

---


## 🌐 Learn More

Visit [omnidim.io](https://www.omnidim.io/) to explore the full platform, UI builder, and templates.

---

## 💬 Support

- Ask in [our Discord](https://discord.gg/kdjzykMTHJ), where engineers from the team answer build questions.
- Bugs and feature requests: [open an issue](https://github.com/Omnidim/omnidim-python-sdk/issues).
- Account or billing: [support@omnidim.io](mailto:support@omnidim.io).

