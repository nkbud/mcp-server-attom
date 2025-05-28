FROM python:3.11-slim

WORKDIR /app

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml README.md /app/
COPY src /app/src/

# Install dependencies and project
RUN uv pip install --system .

# Expose MCP server port
EXPOSE 8000

# Set environment variables (will be overridden by docker run command)
ENV ATTOM_API_KEY=""
ENV LOG_LEVEL=INFO
ENV LOG_FORMAT=json

# Run the server
CMD ["python", "-m", "src.server"]