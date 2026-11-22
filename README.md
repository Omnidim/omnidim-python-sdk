# OmniDimension Python SDK

Python client for the OmniDimension API. Build voice AI agents, place and review calls, run call campaigns and workflows, and manage WhatsApp from code.

Prefer a no-code editor? Use the [web app](https://www.omnidim.io/).

## Installation

```bash
pip install omnidimension
```

## Authentication

Create an API key in the OmniDimension dashboard and set it as an environment variable.

```bash
export OMNIDIM_API_KEY="your_api_key_here"
```

On Windows CMD, use `set OMNIDIM_API_KEY=your_api_key_here`.

```python
import os
from omnidimension import Client

client = Client(os.environ["OMNIDIM_API_KEY"])
```

## Quick start

Create an agent, then dispatch a call to it.

```python
agent = client.agent.create(
    name="Appointment reminder",
    context_breakdown=[
        {"title": "Purpose", "body": "Remind the caller of their appointment.", "is_enabled": True}
    ],
    welcome_message="Hi, this is a reminder about your appointment.",
    call_type="Outgoing",
)

client.call.dispatch_call(agent_id=agent["json"]["id"], to_number="+14155550123")
```

If an agent has no number attached yet, pass `from_number_id` with an ID from `client.phone_number.list()`.

## Error handling

Failed requests raise `APIError` with `status_code` and a message.

```python
from omnidimension import APIError

try:
    client.agent.list()
except APIError as e:
    print(e.status_code, e)
```

## What the SDK sends

Every request carries these headers so we can see which SDK versions and platforms use the API. They name no machine, user or path. You can override any of them by passing your own header.

| Header | Meaning | Example |
|---|---|---|
| `User-Agent` | SDK name and version | `omnidim-python-sdk/<version>` |
| `X-OmniDimension-Lang` | SDK language | `python` |
| `X-OmniDimension-Runtime` | Python implementation | `cpython` |
| `X-OmniDimension-Runtime-Version` | Python version | `3.11.9` |
| `X-OmniDimension-OS` | Operating system | `linux`, `darwin`, `windows` |
| `X-OmniDimension-Arch` | CPU type | `x64`, `arm64` |

When the server sends a request id, `APIError.request_id` holds it and the error message ends with `(request id: ...)`. Quote it when you contact support.

## MCP

Connect an AI assistant to your account with the hosted server at `https://mcp.omnidim.io/mcp`. Setup steps are in the [MCP docs](https://docs.omnidim.io/docs/mcp).

To run a local server instead, use the npm package [`@omnidim-ai/mcp-server`](https://www.npmjs.com/package/@omnidim-ai/mcp-server).

## Guides

- [Python SDK reference](https://docs.omnidim.io/docs/sdks/python)
- [Quickstart](https://docs.omnidim.io/docs/get-started/quickstart)
- [Bulk call campaigns over the API](https://docs.omnidim.io/docs/bulk-calls/api)
- [Phone numbers](https://docs.omnidim.io/docs/get-a-number)
- [Knowledge base](https://docs.omnidim.io/docs/dashboard-guides/knowledge-base)
- [Integrations](https://docs.omnidim.io/docs/integrations)
- [API reference](https://docs.omnidim.io/docs/api-reference)

Reseller accounts: see the [Reseller API docs](https://docs.omnidim.io/docs/reseller-api).

## Support

- Ask in [our Discord](https://discord.gg/kdjzykMTHJ), where engineers from the team answer build questions.
- Bugs and feature requests: [open an issue](https://github.com/Omnidim/omnidim-python-sdk/issues).
- Account or billing: [support@omnidim.io](mailto:support@omnidim.io).
