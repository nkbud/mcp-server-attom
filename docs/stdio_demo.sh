#!/bin/bash

# Demo script for MCP server stdio communication
# This script demonstrates how to communicate with the ATTOM API MCP server via stdio

set -e

echo "=== ATTOM API MCP Server Stdio Communication Demo ==="
echo

# Check if ATTOM_API_KEY is set
if [ -z "$ATTOM_API_KEY" ]; then
    echo "❌ Error: ATTOM_API_KEY environment variable is required"
    echo "   Please set it with: export ATTOM_API_KEY=your_api_key_here"
    exit 1
fi

echo "✅ ATTOM_API_KEY is set"
echo

# Function to send JSON-RPC request and display response
send_request() {
    local request="$1"
    local description="$2"
    
    echo "📤 Sending: $description"
    echo "   Request: $request"
    echo
    
    # Create a temporary file for the request
    local temp_file=$(mktemp)
    echo "$request" > "$temp_file"
    
    echo "📥 Response:"
    
    # Send request via stdio and capture response
    # Timeout after 10 seconds to prevent hanging
    timeout 10s python -m src.server < "$temp_file" 2>/dev/null || {
        echo "   ⚠️  Request timed out or server error (this is expected for demo)"
    }
    
    echo
    echo "---"
    echo
    
    # Clean up
    rm -f "$temp_file"
}

echo "🚀 Starting MCP server stdio communication test..."
echo

# Test 1: Initialize request
INIT_REQUEST='{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "demo-client",
      "version": "1.0.0"
    }
  }
}'

send_request "$INIT_REQUEST" "Initialize Connection"

# Test 2: List tools request
TOOLS_REQUEST='{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}'

send_request "$TOOLS_REQUEST" "List Available Tools"

# Test 3: Property detail request (with demo data)
PROPERTY_REQUEST='{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "property_detail",
    "arguments": {
      "attom_id": "145423726"
    }
  }
}'

send_request "$PROPERTY_REQUEST" "Get Property Details"

echo "✅ Demo completed!"
echo
echo "💡 Notes:"
echo "   - The server logs go to stderr (not shown above)"
echo "   - JSON-RPC responses go to stdout (shown above)"
echo "   - Timeouts are expected in this demo - the server waits for more input"
echo "   - For real usage, keep the connection open and send multiple requests"
echo
echo "🔧 For interactive testing, try:"
echo "   npx @modelcontextprotocol/inspector uvx mcp-server-attom"
echo "   mcp list tools uvx mcp-server-attom"
echo "   mcp call uvx mcp-server-attom property_detail '{\"attom_id\": \"145423726\"}'"