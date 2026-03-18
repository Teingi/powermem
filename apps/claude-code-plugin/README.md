# PowerMem Plugin for Claude Code

Claude Code plugin that connects to [PowerMem](https://github.com/oceanbase/powermem) for intelligent, persistent memory.

## Features

- **MCP integration**: Uses PowerMem MCP Server so Claude can call `add_memory`, `search_memories`, `get_memory_by_id`, `update_memory`, `delete_memory`, `list_memories`.
- **Skills**: `/memory-powermem:remember` and `/memory-powermem:recall` to guide when to store and when to search memories.

## Prerequisites

1. **PowerMem** installed and a running PowerMem backend:
   - Either **MCP Server** (e.g. `uvx powermem-mcp sse` or `uvx powermem-mcp stdio`) with a `.env` in project or home directory.
   - Or **HTTP API Server** (e.g. `powermem-server --host 0.0.0.0 --port 8000`). The plugin's default `.mcp.json` points to `http://localhost:8000/mcp` (MCP over HTTP).

2. **Claude Code** (VS Code extension or CLI) with plugin support.

## Installation

### Option A: Load from directory (development)

```bash
claude --plugin-dir /path/to/powermem/apps/claude-code-plugin
```

### Option B: Install from marketplace

If this plugin is published to a Claude Code plugin marketplace, install it from there.

## Configuration

The default `.mcp.json` in this plugin uses:

- **HTTP transport**: `http://localhost:8000/mcp`

To use a different URL or **stdio** (local MCP process), edit `.mcp.json` in this directory. Example for stdio:

```json
{
  "mcpServers": {
    "powermem": {
      "transport": "stdio",
      "command": "uvx",
      "args": ["powermem-mcp", "stdio"]
    }
  }
}
```

Ensure PowerMem is installed (`pip install powermem`) and a `.env` file is available when using stdio.

## Usage

- In Claude Code, the PowerMem MCP tools are available automatically once the plugin is loaded.
- Use **/memory-powermem:remember** when you want Claude to store something.
- Use **/memory-powermem:recall** when you want Claude to search memories before answering.

## Links

- [PowerMem](https://github.com/oceanbase/powermem)
- [PowerMem MCP docs](https://github.com/oceanbase/powermem/blob/master/docs/api/0004-mcp.md)
