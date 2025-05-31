# MCP Client Integration Guide

This guide explains how to integrate the ATTOM API MCP Server with various MCP clients including Claude Desktop, mcp-inspector, mcp-cli, and direct stdio communication.

## Prerequisites

Before integrating with any MCP client, ensure you have:

1. **Python 3.11 or higher** installed
2. **An ATTOM API key** - Get one from [ATTOM Data Solutions](https://www.attomdata.com/products/api/)
3. **UV package manager** - Install via:
   ```bash
   # Method 1: Via pip (works behind firewalls)
   python -m pip install uv
   
   # Method 2: Via official installer (requires internet access to astral.sh)
   # curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
4. **The mcp-server-attom package** available via:
   ```bash
   # Install globally
   uv tool install mcp-server-attom
   
   # Or run directly without installation
   uvx mcp-server-attom
   ```

> **Note**: If you encounter firewall restrictions accessing `astral.sh`, use the pip installation method for uv instead of the curl installer.

## Environment Setup

Create a `.env` file in your working directory or set environment variables:

```bash
# Required
ATTOM_API_KEY=your_attom_api_key_here

# Optional - customize API endpoints
ATTOM_HOST_URL=https://api.gateway.attomdata.com
LOG_LEVEL=INFO
```

## Claude Desktop Integration

Claude Desktop uses MCP servers through a configuration file that specifies how to start and communicate with the server.

### Configuration

Add the following to your Claude Desktop MCP configuration file:

**For macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**For Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "attom-api": {
      "command": "uvx",
      "args": ["mcp-server-attom"],
      "env": {
        "ATTOM_API_KEY": "your_attom_api_key_here"
      }
    }
  }
}
```

### Alternative Configuration (if uvx is installed globally)

If you have `mcp-server-attom` installed globally via `uv tool install`:

```json
{
  "mcpServers": {
    "attom-api": {
      "command": "mcp-server-attom",
      "env": {
        "ATTOM_API_KEY": "your_attom_api_key_here"
      }
    }
  }
}
```

### Usage in Claude Desktop

Once configured, restart Claude Desktop. You can then use the ATTOM API tools in your conversations:

```
Can you look up property details for 123 Main Street, New York, NY 10001?
```

Claude will automatically use the `property_detail` tool to fetch the information from the ATTOM API.

## MCP Inspector Integration

MCP Inspector is a debugging tool for MCP servers that provides a web interface to test and inspect MCP functionality.

### Installation and Setup

```bash
# Install mcp-inspector
npm install -g @modelcontextprotocol/inspector

# Start the inspector with the ATTOM server
npx @modelcontextprotocol/inspector uvx mcp-server-attom
```

### With Environment Variables

```bash
# Set your API key
export ATTOM_API_KEY=your_attom_api_key_here

# Start inspector
npx @modelcontextprotocol/inspector uvx mcp-server-attom
```

### Usage

1. Open your browser to the URL shown in the terminal (usually `http://localhost:5173`)
2. Use the web interface to:
   - List available tools
   - Test tool calls with different parameters
   - Inspect tool schemas and responses
   - Debug communication issues

## MCP CLI Integration

The MCP CLI provides command-line access to MCP servers for testing and automation.

### Installation

```bash
npm install -g @modelcontextprotocol/cli
```

### Usage

```bash
# Set environment variable
export ATTOM_API_KEY=your_attom_api_key_here

# List available tools
mcp list tools uvx mcp-server-attom

# Call a specific tool
mcp call uvx mcp-server-attom property_detail '{"attom_id": "145423726"}'

# Get property details by address
mcp call uvx mcp-server-attom property_detail '{"address": "123 Main St, New York, NY 10001"}'
```

### Example Commands

```bash
# List all available tools
mcp list tools uvx mcp-server-attom

# Get property details
mcp call uvx mcp-server-attom property_detail '{"attom_id": "145423726"}'

# Get assessment information
mcp call uvx mcp-server-attom assessment_detail '{"attom_id": "145423726"}'

# Get sales history
mcp call uvx mcp-server-attom sales_history_detail '{"attom_id": "145423726"}'

# Get AVM (Automated Valuation Model) data
mcp call uvx mcp-server-attom avm_detail '{"attom_id": "145423726"}'
```

## Direct Stdio Communication

For custom integrations or advanced use cases, you can communicate directly with the MCP server using stdio and JSON-RPC protocol.

### Protocol Overview

The MCP server communicates using JSON-RPC 2.0 over stdio:
- **Input**: JSON-RPC requests via stdin
- **Output**: JSON-RPC responses via stdout
- **Logging**: All logs go to stderr (never stdout)

### Starting the Server

```bash
# Set environment variable
export ATTOM_API_KEY=your_attom_api_key_here

# Start server with stdio transport
uvx mcp-server-attom
```

The server will wait for JSON-RPC messages on stdin and respond on stdout.

### Example Communication

#### 1. Initialize the Connection

Send an initialization request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

#### 2. List Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

#### 3. Call a Tool

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "property_detail",
    "arguments": {
      "attom_id": "145423726"
    }
  }
}
```

### Python Example

```python
import json
import subprocess
import sys

def communicate_with_mcp_server(request):
    """Send a JSON-RPC request to the MCP server and get response."""
    
    # Start the server process
    process = subprocess.Popen(
        ['uvx', 'mcp-server-attom'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={'ATTOM_API_KEY': 'your_api_key_here'}
    )
    
    # Send request
    request_json = json.dumps(request) + '\n'
    stdout, stderr = process.communicate(input=request_json)
    
    # Parse response
    try:
        response = json.loads(stdout.strip())
        return response
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")
        return None

# Example usage
initialize_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "clientInfo": {"name": "python-client", "version": "1.0.0"}
    }
}

response = communicate_with_mcp_server(initialize_request)
print(json.dumps(response, indent=2))
```

### Node.js Example

```javascript
const { spawn } = require('child_process');

function communicateWithMCPServer(request) {
    return new Promise((resolve, reject) => {
        const server = spawn('uvx', ['mcp-server-attom'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            env: { ...process.env, ATTOM_API_KEY: 'your_api_key_here' }
        });

        let stdout = '';
        let stderr = '';

        server.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        server.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        server.on('close', (code) => {
            try {
                const response = JSON.parse(stdout.trim());
                resolve(response);
            } catch (error) {
                reject({ error, stdout, stderr });
            }
        });

        // Send request
        server.stdin.write(JSON.stringify(request) + '\n');
        server.stdin.end();
    });
}

// Example usage
const initializeRequest = {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
        protocolVersion: "2024-11-05",
        capabilities: { tools: {} },
        clientInfo: { name: "node-client", version: "1.0.0" }
    }
};

communicateWithMCPServer(initializeRequest)
    .then(response => console.log(JSON.stringify(response, null, 2)))
    .catch(error => console.error('Error:', error));
```

## Available Tools

The ATTOM API MCP Server provides 23 tools across different categories:

### Property Tools
- `property_address` - Get property address information
- `property_detail` - Get detailed property information  
- `property_basic_profile` - Get basic property profile
- `property_expanded_profile` - Get expanded property profile
- `property_detail_with_schools` - Get property details with school info

### Assessment Tools
- `assessment_detail` - Get detailed assessment information
- `assessment_snapshot` - Get assessment snapshot
- `assessment_history_detail` - Get assessment history

### Sales Tools
- `sale_detail` - Get detailed sales information
- `sale_snapshot` - Get sales snapshot
- `sales_history_detail` - Get sales history
- `sales_history_snapshot` - Get sales history snapshot

### Valuation Tools
- `avm_detail` - Get detailed AVM information
- `avm_snapshot` - Get AVM snapshot
- `avm_history_detail` - Get AVM history
- `attom_avm_detail` - Get ATTOM AVM information
- `home_equity` - Get home equity information
- `rental_avm` - Get rental AVM information

### Event Tools
- `property_event_detail` - Get property event details
- `property_event_history` - Get property event history

### School Tools
- `school_snapshot` - Get school information
- `school_district_snapshot` - Get school district information

### Miscellaneous Tools
- `expand_location` - Expand location information

## Troubleshooting

### Common Issues

1. **Server fails to start**
   - Ensure `ATTOM_API_KEY` environment variable is set
   - Verify Python 3.11+ is installed
   - Check that uv/uvx is available

2. **JSON parsing errors**
   - Ensure all logging goes to stderr, not stdout
   - Verify the server is properly redirecting logs

3. **API key issues**
   - Verify your ATTOM API key is valid
   - Check API key permissions and rate limits

4. **Tool not found errors**
   - Use `tools/list` to see available tools
   - Ensure tool names match exactly (case-sensitive)

5. **Firewall/Network Issues**
   - If you get "blocked by firewall rules" for `astral.sh`, install uv via pip instead:
     ```bash
     python -m pip install uv
     ```
   - This avoids the need to access external installation scripts
   - All package dependencies are available through PyPI

### Debug Mode

Enable debug logging for troubleshooting:

```bash
export LOG_LEVEL=DEBUG
export ATTOM_API_KEY=your_api_key_here
uvx mcp-server-attom
```

### Testing Connection

Use mcp-inspector or mcp-cli to verify the server is working:

```bash
# Quick test with mcp-cli
export ATTOM_API_KEY=your_api_key_here
mcp list tools uvx mcp-server-attom
```

This should return a list of 23 available tools if everything is working correctly.

### Installation Alternatives

If you encounter network restrictions:

```bash
# Alternative 1: Install uv via pip (no external downloads)
python -m pip install uv
uv tool install mcp-server-attom

# Alternative 2: Use system Python and pip directly
pip install mcp-server-attom
python -m mcp_server_attom

# Alternative 3: Install from source
git clone https://github.com/nkbud/mcp-server-attom.git
cd mcp-server-attom
python -m pip install -e .
```