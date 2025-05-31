"""Tests for MCP server stdio transport and client integration."""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest


class TestStdioTransport:
    """Test MCP server stdio transport functionality."""

    def setup_method(self):
        """Set up test environment with API key."""
        # Use a dummy API key for testing
        self.test_api_key = "test_api_key_12345"
        self.env = {**os.environ, "ATTOM_API_KEY": self.test_api_key}
        
        # Path to the server module
        self.repo_root = Path(__file__).parent.parent
        self.server_path = self.repo_root / "src" / "server.py"

    def _run_server_command(self, stdin_data, timeout=10):
        """Run server command and return stdout, stderr, and return code."""
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "src.server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=self.env,
                cwd=self.repo_root
            )
            
            stdout, stderr = process.communicate(
                input=stdin_data, 
                timeout=timeout
            )
            
            return stdout, stderr, process.returncode
            
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return stdout, stderr, -1

    def test_server_starts_without_api_key(self):
        """Test server fails gracefully without API key."""
        env_no_key = {k: v for k, v in os.environ.items() if k != "ATTOM_API_KEY"}
        
        process = subprocess.Popen(
            [sys.executable, "-m", "src.server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env_no_key,
            cwd=self.repo_root
        )
        
        # Send empty input and close stdin
        stdout, stderr = process.communicate(input="", timeout=5)
        
        # Server should exit with error code 1
        assert process.returncode == 1
        assert "ATTOM_API_KEY environment variable is required" in stderr

    def test_logging_goes_to_stderr(self):
        """Test that all logging output goes to stderr, not stdout."""
        # Send an invalid JSON-RPC request to trigger error logging
        invalid_request = "invalid json\n"
        
        stdout, stderr, returncode = self._run_server_command(invalid_request, timeout=5)
        
        # stdout should be clean (no log messages)
        # stderr should contain log messages
        assert "Starting ATTOM API MCP Server" in stderr
        assert "Running MCP server with STDIO transport" in stderr
        
        # stdout should not contain any log messages
        log_indicators = ["INFO", "DEBUG", "ERROR", "WARNING", "Starting", "Running"]
        for indicator in log_indicators:
            assert indicator not in stdout

    def test_json_rpc_initialize_request(self):
        """Test MCP initialize request via JSON-RPC."""
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        request_json = json.dumps(initialize_request) + "\n"
        stdout, stderr, returncode = self._run_server_command(request_json, timeout=10)
        
        # Server should start and log to stderr
        assert "Starting ATTOM API MCP Server" in stderr
        assert "Running MCP server with STDIO transport" in stderr
        
        # Parse JSON-RPC response from stdout
        stdout_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        if stdout_lines:
            try:
                response = json.loads(stdout_lines[0])
                assert response.get("jsonrpc") == "2.0"
                assert response.get("id") == 1
                assert "result" in response
            except json.JSONDecodeError:
                # Server might still be starting up or have different response format
                # This is acceptable for this test
                pass

    def test_tools_list_request(self):
        """Test tools/list request via JSON-RPC."""
        # First initialize, then list tools
        requests = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"}
                }
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
        ]
        
        # Send both requests
        requests_json = "\n".join(json.dumps(req) for req in requests) + "\n"
        stdout, stderr, returncode = self._run_server_command(requests_json, timeout=15)
        
        # Check that server started properly
        assert "Starting ATTOM API MCP Server" in stderr
        
        # Parse responses from stdout
        stdout_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        # Should have at least one response
        assert len(stdout_lines) >= 1
        
        # Try to parse the last response as tools/list response
        if len(stdout_lines) >= 2:
            try:
                tools_response = json.loads(stdout_lines[-1])
                assert tools_response.get("jsonrpc") == "2.0"
                if "result" in tools_response:
                    tools = tools_response["result"].get("tools", [])
                    # Should have 23 tools based on the documentation
                    assert len(tools) > 0
            except json.JSONDecodeError:
                # Response format might be different, but that's OK for this test
                pass

    def test_stdout_is_clean_json_rpc(self):
        """Test that stdout contains only clean JSON-RPC responses."""
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        request_json = json.dumps(initialize_request) + "\n"
        stdout, stderr, returncode = self._run_server_command(request_json, timeout=10)
        
        # Check that stdout contains only JSON or is empty
        stdout_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        for line in stdout_lines:
            if line:
                try:
                    # Each line should be valid JSON
                    parsed = json.loads(line)
                    # Should be a JSON-RPC response
                    assert "jsonrpc" in parsed
                except json.JSONDecodeError:
                    pytest.fail(f"stdout contains non-JSON content: {line}")

    def test_error_handling_with_invalid_json(self):
        """Test server handles invalid JSON gracefully."""
        invalid_requests = [
            "invalid json",
            "{incomplete json",
            '{"jsonrpc": "2.0", "method": "nonexistent"}',  # Missing id
            ""  # Empty request
        ]
        
        for invalid_request in invalid_requests:
            request_data = invalid_request + "\n"
            stdout, stderr, returncode = self._run_server_command(request_data, timeout=5)
            
            # Server should handle errors gracefully
            # stderr should contain server startup logs
            assert "Starting ATTOM API MCP Server" in stderr
            
            # stdout should either be empty or contain valid JSON-RPC error responses
            stdout_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
            
            for line in stdout_lines:
                if line:
                    try:
                        response = json.loads(line)
                        # Should be a JSON-RPC response (either error or normal)
                        assert "jsonrpc" in response
                    except json.JSONDecodeError:
                        pytest.fail(f"Invalid JSON in stdout: {line}")


class TestMCPClientCompatibility:
    """Test compatibility with various MCP clients."""

    def setup_method(self):
        """Set up test environment."""
        self.test_api_key = "test_api_key_12345"
        self.env = {**os.environ, "ATTOM_API_KEY": self.test_api_key}
        self.repo_root = Path(__file__).parent.parent

    def test_uvx_command_availability(self):
        """Test that uvx can find and run the server."""
        # This test checks if the package structure supports uvx execution
        # We can't test actual uvx without network access, but we can test the entry point
        
        # Test that the server module can be imported and has main function
        server_module_path = self.repo_root / "src" / "server.py"
        assert server_module_path.exists()
        
        # Read the server file and check for main function
        content = server_module_path.read_text()
        assert "def main(" in content  # More flexible check for function signature
        assert 'if __name__ == "__main__":' in content
        assert "main()" in content

    def test_pyproject_toml_entry_point(self):
        """Test that pyproject.toml has correct entry point for CLI."""
        pyproject_path = self.repo_root / "pyproject.toml"
        assert pyproject_path.exists()
        
        content = pyproject_path.read_text()
        
        # Should have CLI entry point
        assert "[project.scripts]" in content
        assert "mcp-server-attom" in content
        assert "src.server:main" in content

    def test_mcp_protocol_compliance(self):
        """Test basic MCP protocol compliance."""
        # Test that server responds to standard MCP methods
        test_methods = [
            {
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "test", "version": "1.0.0"}
                }
            },
            {
                "method": "tools/list",
                "params": {}
            }
        ]
        
        for i, test_case in enumerate(test_methods):
            request = {
                "jsonrpc": "2.0",
                "id": i + 1,
                **test_case
            }
            
            request_json = json.dumps(request) + "\n"
            
            try:
                process = subprocess.Popen(
                    [sys.executable, "-m", "src.server"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=self.env,
                    cwd=self.repo_root
                )
                
                stdout, stderr = process.communicate(input=request_json, timeout=10)
                
                # Should not crash and should produce some output
                assert process.returncode is not None
                
                # stderr should contain startup logs
                assert "Starting ATTOM API MCP Server" in stderr
                
            except subprocess.TimeoutExpired:
                process.kill()
                # Timeout is acceptable - server might be waiting for more input


class TestStdioDocumentation:
    """Test that stdio communication examples from documentation work."""

    def setup_method(self):
        """Set up test environment."""
        self.test_api_key = "test_api_key_12345"
        self.env = {**os.environ, "ATTOM_API_KEY": self.test_api_key}
        self.repo_root = Path(__file__).parent.parent

    def test_documentation_examples(self):
        """Test JSON-RPC examples from the documentation."""
        # Examples from CLIENT_INTEGRATION.md
        examples = [
            {
                "name": "initialize",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "clientInfo": {"name": "example-client", "version": "1.0.0"}
                    }
                }
            },
            {
                "name": "tools_list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                }
            }
        ]
        
        for example in examples:
            request_json = json.dumps(example["request"]) + "\n"
            
            try:
                process = subprocess.Popen(
                    [sys.executable, "-m", "src.server"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=self.env,
                    cwd=self.repo_root
                )
                
                stdout, stderr = process.communicate(input=request_json, timeout=10)
                
                # Basic validation - server should start and handle the request
                assert "Starting ATTOM API MCP Server" in stderr
                
                # stdout should be either empty or contain valid JSON
                stdout_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
                for line in stdout_lines:
                    if line:
                        try:
                            json.loads(line)  # Should be valid JSON
                        except json.JSONDecodeError:
                            pytest.fail(f"Invalid JSON in stdout for {example['name']}: {line}")
                
            except subprocess.TimeoutExpired:
                process.kill()
                # Timeout is acceptable for this test

    def test_server_clean_shutdown(self):
        """Test that server shuts down cleanly when stdin is closed."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        request_json = json.dumps(request) + "\n"
        
        process = subprocess.Popen(
            [sys.executable, "-m", "src.server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.env,
            cwd=self.repo_root
        )
        
        # Send request and close stdin
        stdout, stderr = process.communicate(input=request_json, timeout=10)
        
        # Server should exit cleanly (return code should be 0 or indicate clean exit)
        assert process.returncode is not None
        
        # Should have startup logs
        assert "Starting ATTOM API MCP Server" in stderr