# ATTOM API MCP Server

An MCP server for the ATTOM API, providing real estate data via the MCP protocol. This server acts as middleware, exposing the ATTOM API endpoints as MCP tools that can be used by AI agents.

## Features

- MCP interface for ATTOM API endpoints
- Comprehensive API coverage for property data, valuations, assessments, and sales
- Structured error handling and logging
- Configurable via environment variables
- Packaged as a UVX tool for easy deployment

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- An ATTOM API key

## Installation

### Local Development

1. Clone this repository:

```bash
git clone https://github.com/nkbud/mcp-server-attom.git
cd mcp-server-attom
```

2. Install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Create a `.env` file with your ATTOM API key:

```bash
cp .env.example .env
# Edit .env and add your ATTOM API key
```

### UVX Installation

To install the tool using UVX:

```bash
uvx install attom-api
```

Then configure it in your UVX tool configuration (e.g., `claude-desktop.yaml`):

```yaml
tools:
  - name: attom-api
    env:
      ATTOM_API_KEY: your_api_key_here
```

## Usage

### Running Locally

Start the server:

```bash
python -m src.server
```

This will start the server on `http://localhost:8000`.

### Making Requests

The server exposes MCP tools for various ATTOM API endpoints. Here's an example of using the property_detail tool:

```python
await mcp.tools.property_detail(
    attom_id="145423726"  # OR
    # address="123 Main St, New York, NY 10001"  # OR
    # address1="123 Main St", address2="New York, NY 10001"  # OR
    # fips="36061", apn="12345"
)
```

## Configuration

The server can be configured using the following environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| ATTOM_API_KEY | Your ATTOM API key | Yes | - |
| ATTOM_HOST_URL | Base URL for the ATTOM API | No | https://api.gateway.attomdata.com |
| ATTOM_PROP_API_PREFIX | Prefix for property API endpoints | No | /propertyapi/v1.0.0 |
| ATTOM_DLP_V2_PREFIX | Prefix for DLP v2 API endpoints | No | /property/v2 |
| ATTOM_DLP_V3_PREFIX | Prefix for DLP v3 API endpoints | No | /property/v3 |
| LOG_LEVEL | Logging level (DEBUG, INFO, WARNING, ERROR) | No | INFO |
| LOG_FORMAT | Log format (json or console) | No | json |

## Available Tools

### Property Tools

- `property_address`: Get property address information
- `property_detail`: Get detailed property information
- `property_basic_profile`: Get basic property profile information
- `property_expanded_profile`: Get expanded property profile information
- `property_detail_with_schools`: Get property details including school information

### Assessment Tools

- `assessment_detail`: Get detailed assessment information
- `assessment_snapshot`: Get assessment snapshot
- `assessment_history_detail`: Get assessment history

### Sale Tools

- `sale_detail`: Get detailed sales information
- `sale_snapshot`: Get sales snapshot
- `sales_history_detail`: Get sales history
- `sales_history_snapshot`: Get sales history snapshot

### Valuation Tools

- `avm_detail`: Get detailed AVM information
- `avm_snapshot`: Get AVM snapshot
- `avm_history_detail`: Get AVM history
- `attom_avm_detail`: Get ATTOM AVM information
- `home_equity`: Get home equity information
- `rental_avm`: Get rental AVM information

## Development

### Running Tests

```bash
uv pip install -e ".[test]"
pytest
```

### Linting

```bash
uv pip install -e ".[dev]"
ruff check .
black .
isort .
```

## License

MIT

## Support

For issues with this MCP server, please open an issue on the [GitHub repository](https://github.com/nkbud/mcp-server-attom/issues).

For issues with the ATTOM API itself, please contact ATTOM Data Solutions support.