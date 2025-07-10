# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is an MCP (Model Context Protocol) playground repository containing tutorial examples for building MCP servers and clients. The repository is organized into 4 main components:

1. **weather-server-python/** - A Python MCP server using FastMCP that provides weather data via NWS API
2. **weather-server-typescript/** - A TypeScript MCP server equivalent using the MCP SDK
3. **mcp-client-python/** - A Python MCP client that connects to servers and provides an LLM-powered chatbot interface
4. **mcp-client-typescript/** - A TypeScript MCP client equivalent

## Key Components

### MCP Servers
Both weather servers implement the same functionality:
- `get_alerts(state)` - Get weather alerts for a US state (2-letter code)
- `get_forecast(latitude, longitude)` - Get weather forecast for coordinates

### MCP Clients
Both clients provide:
- Connection to MCP servers (Python or JavaScript)
- Integration with Anthropic's Claude API
- Interactive chat loop for querying weather data through the connected server

## Development Commands

### Python Components

**Weather Server (Python)**:
```bash
cd weather-server-python
python weather.py
```

**MCP Client (Python)**:
```bash
cd mcp-client-python
python client.py ../weather-server-python/weather.py
```

### TypeScript Components

**Weather Server (TypeScript)**:
```bash
cd weather-server-typescript
npm run build
node build/index.js
```

**MCP Client (TypeScript)**:
```bash
cd mcp-client-typescript
npm run build
node build/index.js ../weather-server-typescript/build/index.js
```

## Environment Setup

Both clients require an `ANTHROPIC_API_KEY` environment variable. Create a `.env` file in the respective client directories:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Package Management

- Python projects use `pyproject.toml` with uv for dependency management
- TypeScript projects use `package.json` with npm
- All dependencies are already configured in the respective configuration files

## Running Examples

To test the complete MCP flow:
1. Start a weather server in one terminal
2. Start the corresponding client in another terminal, passing the server script path
3. Query weather data through the interactive chat interface

The clients will automatically discover and use the tools provided by the connected MCP server.