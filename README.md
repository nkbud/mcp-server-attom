# ATTOM API MCP Server

An MCP server for the ATTOM API, providing real estate data via the MCP protocol. This server acts as middleware, exposing the ATTOM API endpoints as MCP tools that can be used by AI agents.

## Features

- MCP interface for ATTOM API endpoints
- Comprehensive API coverage for property data, valuations, assessments, and sales
- Structured error handling and logging
- Configurable via environment variables
- Packaged as a Python CLI tool for easy deployment

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- An ATTOM API key

## Installation

### Using UVX (Recommended)

The easiest way to install and run the ATTOM API MCP Server is via `uvx`:

```bash
uvx mcp-server-attom --help
```

This will download and run the tool directly without requiring a permanent installation.

To install it permanently:

```bash
uv tool install mcp-server-attom
```

### Local Development

1. Clone this repository:

```bash
git clone https://github.com/nkbud/mcp-server-attom.git
cd mcp-server-attom
```

2. Install dependencies:

```bash
uv sync --locked --all-extras --dev
```

3. Create a `.env` file with your ATTOM API key:

```bash
cp .env.example .env
# Edit .env and add your ATTOM API key
```

## Usage

### Running as a CLI Tool

Start the server using the `mcp-server-attom` command:

```bash
# If installed via uv tool install
mcp-server-attom --port 8000 --host 0.0.0.0

# Or run directly via uvx
uvx mcp-server-attom --port 8000 --host 0.0.0.0
```

Available command-line options:
- `--host`: Host to bind the server to (default: 0.0.0.0)
- `--port`: Port to bind the server to (default: 8000)
- `--log-level`: Logging level (debug, info, warning, error)
- `--reload`: Enable auto-reload on code changes

### Running Locally During Development

Start the server during development:

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
uv run pytest
```

### Linting

```bash
uv run ruff check .
uv run black .
uv run isort .
```

### Building and Publishing

To build and publish the package to PyPI:

1. Ensure you have the latest version of `uv`:

```bash
pip install -U uv
```

2. Set up a PyPI token:

   - Create an account on [PyPI](https://pypi.org/) if you don't have one
   - Go to Account Settings > API Tokens
   - Create a token with scope restricted to the `mcp-server-attom` project
   - Save the token securely

3. Build the package:

```bash
uv build --no-sources
```

4. Publish the package using your PyPI token:

```bash
uv publish --token YOUR_PYPI_TOKEN
```

Alternatively, you can store your token in a `.pypirc` file or as an environment variable:

```bash
export PYPI_TOKEN=YOUR_PYPI_TOKEN
uv publish
```

## License

MIT

## Support

For issues with this MCP server, please open an issue on the [GitHub repository](https://github.com/nkbud/mcp-server-attom/issues).

For issues with the ATTOM API itself, please contact ATTOM Data Solutions support.