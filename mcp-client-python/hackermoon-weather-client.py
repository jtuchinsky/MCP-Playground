import subprocess
import json
from sys import stderr
from dotenv import load_dotenv

load_dotenv()

class HackermoonWeatherClient:
    def __init__(self, server_script_path="weather.py"):
        """Initialize the client and start the MCP server subprocess."""
        print("🌙 HackerMoon Weather Client Initializing...")
        
        # Start the weather.py process
        # Use python directly to execute the script
        # Redirect stdin, stdout to PIPE for communication
        self.process = subprocess.Popen(
            ["python", server_script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr
        )
        
        # Define common MCP requests
        self.requests = {
            'init': {
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "HackermoonWeatherClient", "version": "1.0.0"}
                }
            },
            'initialized': {
                "jsonrpc": "2.0", "method": "notifications/initialized"
            },
            'list_tools': {
                "jsonrpc": "2.0", "id": 2, "method": "tools/list"
            }
        }
        
        print("🔧 Subprocess started successfully!")

    def _send_mcp_request(self, process, request):
        """Sends a JSON-RPC request to the subprocess's stdin."""
        json_request = json.dumps(request) + '\n'  # Add newline delimiter
        process.stdin.write(json_request.encode('utf-8'))
        process.stdin.flush()  # Ensure the data is sent immediately

    def _read_mcp_response(self):
        """Reads a JSON-RPC response from the subprocess's stdout."""
        # Assuming the server sends one JSON object per line
        line = self.process.stdout.readline().decode('utf-8')
        if line:
            print(f"📡 Response length: {len(line)} chars")
            return json.loads(line)
        return None

    def initialize_connection(self):
        """Initialize the MCP connection with the server."""
        print("🤝 Sending initialize request...")
        self._send_mcp_request(self.process, self.requests['init'])
        init_response = self._read_mcp_response()
        
        print("📨 Sending initialized notification...")
        self._send_mcp_request(self.process, self.requests['initialized'])
        
        return init_response

    def list_tools(self):
        """List available tools from the MCP server."""
        print("🔍 Requesting available tools...")
        self._send_mcp_request(self.process, self.requests['list_tools'])
        return self._read_mcp_response()

    def call_tool(self, tool_name, arguments):
        """Call a specific tool with given arguments."""
        call_request = {
            "jsonrpc": "2.0", 
            "id": 3, 
            "method": "tools/call",
            "params": {
                "name": tool_name, 
                "arguments": arguments
            }
        }
        
        print(f"⚡ Calling tool: {tool_name}")
        self._send_mcp_request(self.process, call_request)
        return self._read_mcp_response()

    def cleanup(self):
        """Clean up the subprocess."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("🌙 HackerMoon client terminated gracefully")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


def main():
    # Example usage
    with HackermoonWeatherClient() as client:
        # Initialize connection
        init_resp = client.initialize_connection()
        print("✅ Init response:", init_resp)
        
        # List available tools
        tools_resp = client.list_tools()
        print("🛠️  Available tools:", tools_resp)
        
        # Example tool call
        alerts_resp = client.call_tool("get_alerts", {"state": "TX"})
        print("🌩️  Weather alerts:", alerts_resp)


if __name__ == "__main__":
    main()