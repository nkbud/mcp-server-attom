# ATTOM API Server

A FastMCP server implementation of the ATTOM API based on the `api.json` specification.

## Features

- Full implementation of ATTOM API routes from the Postman collection
- Property API endpoints for property details, snapshots, assessment, sales, AVM, etc.
- Area API endpoints for geographic boundaries and lookups
- POI API for searching points of interest
- Community and School API endpoints
- API Key authentication
- Comprehensive error handling
- Mock data for demonstration purposes

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

The server will start on `http://localhost:8000` by default.

## Configuration

Configuration is loaded from environment variables. You can create a `.env` file in the root directory with these settings:

```
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
API_KEYS=your_api_key_1,your_api_key_2
```

## API Authentication

All API endpoints are protected with API Key authentication. Include your API key in the `apikey` header:

```
apikey: your_api_key
```

## API Documentation

Access the API documentation when running the server by navigating to `/docs` in your browser.

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT