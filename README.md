# ATTOM API Server using FastMCP

An implementation of the ATTOM API as a set of FastMCP tools, based on the `api.json` specification.

## Features

- Implementation of ATTOM API functionality as FastMCP tools
- Property API tools for property details, snapshots, assessments, sales, AVM, etc.
- Area API tools for geographic boundaries and lookups
- POI API tools for searching points of interest
- Community and School API tools
- API Key authentication
- Comprehensive error handling
- Mock data for demonstration purposes

## What is FastMCP?

FastMCP is a framework for building AI-powered servers using the Model Control Protocol (MCP). Unlike traditional REST API frameworks, FastMCP uses a tool-based approach where endpoints are defined as "tools" that can be invoked by clients.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nkbud/mcp-server-attom.git
   cd mcp-server-attom
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Run the server with:

```bash
python -m app.main
```

The server will start and be available for connections.

## Configuration

Configuration is loaded from environment variables. You can create a `.env` file in the root directory with these settings:

```
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=INFO
API_KEYS=your_api_key_1,your_api_key_2
```

## API Authentication

All API tools require API Key authentication. When making requests to the server, include your API key in the `apikey` header:

```
apikey: your_api_key
```

## Available Tools

The server provides the following FastMCP tools:

### Property Tools
- `property_detail` - Get detailed information about a property
- `property_snapshot` - Get a basic snapshot of property information
- `property_search` - Search for properties by various criteria

### Area Tools
- `boundary_detail` - Get boundary details for a geographic area
- `hierarchy_lookup` - Look up geographic hierarchy for a location

### POI Tools
- `poi_search` - Search for points of interest
- `poi_category_lookup` - Look up POI categories

### Community Tools
- `neighborhood_community` - Get neighborhood community information
- `location_lookup` - Look up locations by various criteria

### School Tools
- `school_profile` - Get school profile information
- `school_district` - Get school district information
- `school_search` - Search for schools

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT