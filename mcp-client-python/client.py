import subprocess
from sys import stderr

from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env

# Behold! We create life!
# (fork off an MCP subprocess)
# Start the weather.py process
# Use `uv run` to execute the script in the uv environment
# Redirect stdin, stdout to PIPE for communication
# Redirect stderr to DEVNULL to suppress error messages

# Behold! We create life!
process = subprocess.Popen(
    ["uv", "run", "weather.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL  # Silence the screams
)

# Every good relationship starts with mutual identification.
# We will start by announcing ourselves (like a gentleman):
# Define the 'initialize' request
init_request = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "clientInfo": {
      "name": "MyMCPClient",
      "version": "1.0.0"
    }
  }
}

#This is our opening salvo—the first packet we send to establish communication.
# It tells the server three crucial things:
# - we speak MCP,
# - which version we're using,
# - and what capabilities we bring to the table.

# You'll notice this follows the JSON-RPC 2.0 format, and that's going to be consistent
# throughout our entire conversation with the server.
# Every message, every response—all JSON-RPC 2.0.

# Let's fire it off
def send_mcp_request(process, request):
    """Sends a JSON-RPC request to the subprocess's stdin."""
    json_request = json.dumps(request) + '\n' # Add newline delimiter
    process.stdin.write(json_request.encode('utf-8'))
    process.stdin.flush() # Ensure the data is sent immediately


# 1. Send the initialize request
print("Sending initialize request...")
send_mcp_request(process, init_request)