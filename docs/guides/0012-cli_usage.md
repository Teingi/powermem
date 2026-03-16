# SeekMem CLI Usage Guide

This guide describes how to use the SeekMem Command Line Interface (CLI) introduced in SeekMem 1.0.0. The CLI provides a full set of memory operations, configuration management, backup/restore, and an interactive shell—all from the terminal.

## Table of Contents

- [Installation and Invocation](#installation-and-invocation)
- [Global Options](#global-options)
- [Command Overview](#command-overview)
- [Memory Commands](#memory-commands)
- [Configuration Commands](#configuration-commands)
- [Statistics](#statistics)
- [Management Commands](#management-commands)
- [Interactive Shell](#interactive-shell)
- [Shell Completion](#shell-completion)

---

## Installation and Invocation

After installing SeekMem, the CLI is available as:

- **`smem`** – primary entry point (when installed as a console script)
- **`seekmem-cli`** – alternative entry point

```bash
# Ensure SeekMem is installed
pip install seekmem

# Check version and help
smem --version
smem --help
```

If no subcommand is given, the CLI prints "Missing command." and shows the main help.

---

## Global Options

These options can be used before any subcommand (and some are also available per-subcommand where noted).

| Option | Short | Description |
|--------|-------|-------------|
| `--env-file PATH` | `-e` | Path to a `.env` configuration file. Overrides the default (e.g. `./.env`). |
| `--json` | `-j` | Output results in JSON format. |
| `--verbose` | `-v` | Enable verbose output (e.g. stack traces on errors). |
| `--install-completion SHELL` | — | Install shell completion for `bash`, `zsh`, `fish`, or `powershell`. |
| `--version` | — | Show CLI version. |
| `--help` | `-h` | Show help. |

**Examples:**

```bash
smem -e .env.production memory list
smem --json stats
smem -v memory add "User prefers dark mode" --user-id user123
smem --install-completion bash
```

---

## Command Overview

| Command Group | Subcommands | Description |
|---------------|-------------|-------------|
| **memory** | add, search, get, update, delete, list, delete-all | CRUD and search for memories. |
| **config** | show, validate, test, init | View, validate, test, and initialize configuration. |
| **stats** | (none) | Display memory statistics. |
| **manage** | backup, restore, cleanup, migrate | Backup, restore, cleanup, and migrate data. |
| **shell** | (none) | Start interactive mode (REPL). |

---

## Memory Commands

All memory commands run under the `memory` group and use the same backend as the Python SDK (same config and storage).

### `smem memory add CONTENT`

Add a new memory. Content can be a single fact or short description; with inference enabled (default), the system may deduplicate or merge with existing memories.

**Arguments:**

- `CONTENT` (required): The memory content (e.g. a sentence or short paragraph).

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | User ID for the memory. |
| `--agent-id AGENT_ID` | `-a` | Agent ID for the memory. |
| `--run-id RUN_ID` | `-r` | Run/session ID. |
| `--metadata JSON` | `-m` | Metadata as a JSON string, e.g. `'{"key": "value"}'`. |
| `--scope SCOPE` | — | One of: `private`, `agent_group`, `user_group`, `public`. |
| `--memory-type TYPE` | — | One of: `working`, `short_term`, `long_term`. |
| `--no-infer` | — | Disable intelligent inference (no dedup/merge). |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem memory add "User prefers dark mode" --user-id user123
smem memory add "API key is stored in vault" -m '{"category": "security"}'
smem memory add "Meeting at 3pm Friday" -u user1 -a agent1 --no-infer
```

---

### `smem memory search QUERY`

Search memories by semantic similarity to the given query.

**Arguments:**

- `QUERY` (required): Search query text.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | Filter by user ID. |
| `--agent-id AGENT_ID` | `-a` | Filter by agent ID. |
| `--run-id RUN_ID` | `-r` | Filter by run/session ID. |
| `--limit N` | `-l` | Maximum number of results (default: 10). |
| `--threshold T` | `-t` | Minimum similarity score (e.g. `0.3`). |
| `--filters JSON` | `-f` | Additional filters as JSON. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem memory search "user preferences" --user-id user123
smem memory search "dark mode" -l 5 -j
smem memory search "123" -t 0.3
```

---

### `smem memory get MEMORY_ID`

Retrieve a single memory by its global ID. Optional `--user-id` / `--agent-id` enforce access control (memory is returned only if it belongs to that user/agent).

**Arguments:**

- `MEMORY_ID` (required): Numeric memory ID.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | User ID for access control. |
| `--agent-id AGENT_ID` | `-a` | Agent ID for access control. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem memory get 123456789
smem memory get 123456789 --user-id user123
```

---

### `smem memory update MEMORY_ID CONTENT`

Update an existing memory’s content (and optionally metadata).

**Arguments:**

- `MEMORY_ID` (required): Numeric memory ID.
- `CONTENT` (required): New content.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | User ID for access control. |
| `--agent-id AGENT_ID` | `-a` | Agent ID for access control. |
| `--metadata JSON` | `-m` | New metadata as JSON. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem memory update 123456789 "Updated content"
smem memory update 123456789 "New content" -m '{"updated": true}'
```

---

### `smem memory delete MEMORY_ID`

Delete a memory by ID. Prompts for confirmation unless `--yes` is used.

**Arguments:**

- `MEMORY_ID` (required): Numeric memory ID.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | User ID for access control. |
| `--agent-id AGENT_ID` | `-a` | Agent ID for access control. |
| `--yes` | `-y` | Skip confirmation. |

**Examples:**

```bash
smem memory delete 123456789
smem memory delete 123456789 --yes
```

---

### `smem memory list`

List memories with optional filters, pagination, and sorting.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | Filter by user ID. |
| `--agent-id AGENT_ID` | `-a` | Filter by agent ID. |
| `--run-id RUN_ID` | `-r` | Filter by run ID. |
| `--limit N` | `-l` | Maximum results (default: 50). |
| `--offset N` | `-o` | Offset for pagination (default: 0). |
| `--sort-by FIELD` | `-s` | Sort by: `created_at`, `updated_at`, `id` (default: `created_at`). |
| `--order ORDER` | — | `asc` or `desc` (default: `desc`). |
| `--filters JSON` | `-f` | Additional filters as JSON. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem memory list --user-id user123
smem memory list -l 20 -o 0
smem memory list --sort-by created_at --order desc
```

---

### `smem memory delete-all`

Delete all memories matching the given filters. **Irreversible.** Requires `--confirm` and an interactive confirmation.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | Filter by user ID. |
| `--agent-id AGENT_ID` | `-a` | Filter by agent ID. |
| `--run-id RUN_ID` | `-r` | Filter by run ID. |
| `--confirm` | — | **Required.** Acknowledge bulk deletion. |

**Examples:**

```bash
smem memory delete-all --user-id user123 --confirm
smem memory delete-all --run-id session1 --confirm
```

---

## Configuration Commands

Configuration commands use the same `.env`-based setup as the SDK. Use `--env-file` to point to a specific file.

### `smem config show`

Display current configuration (from the chosen `.env` file). Sensitive values (e.g. API keys, passwords) are masked unless `--show-secrets` is used.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--section SECTION` | `-s` | Section to show: `llm`, `embedder`, `vector_store`, `graph_store`, `intelligent_memory`, `agent_memory`, `reranker`, or `all` (default). |
| `--show-secrets` | — | Show API keys and passwords (use with caution). |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem config show
smem config show --section llm
smem config show -j
```

---

### `smem config validate`

Validate the configuration file. Reports errors and optional warnings; with `--strict`, more checks are enforced.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--env-file PATH` | `-f` | Path to `.env` file to validate. |
| `--strict` | — | Enable strict validation. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem config validate
smem config validate -f .env.production
smem config validate --strict
```

---

### `smem config test`

Test connectivity for database, LLM, and embedder (using the current config).

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--component COMPONENT` | `-c` | One of: `database`, `llm`, `embedder`, `all` (default). |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem config test
smem config test -c database
smem config test -c llm
```

---

### `smem config init`

Run an interactive configuration wizard that creates or updates a `.env` file. Supports quickstart (minimal prompts) or custom (full) mode.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--env-file PATH` | `-f` | Target `.env` file (default: auto-detected or `./.env`). |
| `--dry-run` | — | Show planned changes without writing. |
| `--test` / `--no-test` | — | Run validation and connectivity tests after writing (default: no). |
| `--component COMPONENT` | `-c` | When `--test` is used: `database`, `llm`, `embedder`, or `all`. |

**Examples:**

```bash
smem config init
smem config init -f .env
smem config init --test --component database
```

---

## Statistics

### `smem stats`

Display memory statistics (total counts, distribution by type, age, etc.). Optional filters apply to the same backend as other memory commands.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--user-id USER_ID` | `-u` | Filter by user ID. |
| `--agent-id AGENT_ID` | `-a` | Filter by agent ID. |
| `--detailed` | `-d` | Show more detailed statistics. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem stats
smem stats -u user123
smem stats --agent-id agent1 -j
smem stats --detailed
```

---

## Management Commands

### `smem manage backup`

Export memories to a JSON file. Filters and limit control which memories are included.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--output PATH` | `-o` | Output file (default: `seekmem_backup_<timestamp>.json`). |
| `--user-id USER_ID` | `-u` | Filter by user ID. |
| `--agent-id AGENT_ID` | `-a` | Filter by agent ID. |
| `--run-id RUN_ID` | `-r` | Filter by run ID. |
| `--limit N` | `-l` | Maximum memories to export (default: 10000). |
| `--include-metadata` | — | Include metadata (default: true). |
| `--json` | `-j` | Output status in JSON. |

**Examples:**

```bash
smem manage backup -o backup.json
smem manage backup --user-id user123 -o user_backup.json
smem manage backup -l 1000
```

---

### `smem manage restore`

Import memories from a JSON backup file produced by `smem manage backup`. Can override user/agent IDs and skip duplicates.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--input PATH` | `-i` | **Required.** Input backup file. |
| `--user-id USER_ID` | `-u` | Override user ID for all restored memories. |
| `--agent-id AGENT_ID` | `-a` | Override agent ID for all restored memories. |
| `--dry-run` | — | Preview restore without writing. |
| `--skip-duplicates` | — | Skip memories that already exist (default: true). |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem manage restore -i backup.json
smem manage restore -i backup.json --dry-run
smem manage restore -i backup.json -u new_user
```

---

### `smem manage cleanup`

Remove or archive memories with low retention scores (Ebbinghaus-based). Use `--dry-run` to preview.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--threshold T` | `-t` | Retention score below which to delete (default: 0.1). |
| `--archive-threshold T` | — | Retention score below which to archive (default: 0.3). |
| `--user-id USER_ID` | `-u` | Filter by user ID. |
| `--agent-id AGENT_ID` | `-a` | Filter by agent ID. |
| `--dry-run` | — | Preview only, no changes. |
| `--force` | `-f` | Skip confirmation. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem manage cleanup --dry-run
smem manage cleanup --threshold 0.2
smem manage cleanup -u user123 --force
```

---

### `smem manage migrate`

Migrate data between stores (e.g. main store and sub-stores). Availability depends on the storage backend.

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--target-store INDEX` | `-t` | **Required.** Target sub-store index. |
| `--source-store INDEX` | `-s` | Source sub-store index (default: main store). |
| `--delete-source` | — | Delete from source after migration. |
| `--dry-run` | — | Preview only. |
| `--json` | `-j` | Output in JSON. |

**Examples:**

```bash
smem manage migrate -t 0 --dry-run
smem manage migrate -t 1 --delete-source
```

---

## Interactive Shell

### `smem shell`

Start an interactive REPL (Read-Eval-Print Loop) for SeekMem. You can run memory and stats commands without typing `smem memory` or `smem stats` each time, and set default `user_id` / `agent_id` for the session.

**Commands inside the shell:**

| Command | Description |
|---------|-------------|
| `add <content> [--user-id id] [--agent-id id]` | Add a memory. |
| `search <query> [--user-id id] [--limit n] [--threshold t]` | Search memories. |
| `get <memory_id> [--user-id id]` | Get a memory by ID. |
| `update <memory_id> <content> [--user-id id]` | Update a memory. |
| `delete <memory_id> [--user-id id]` | Delete a memory. |
| `list [--user-id id] [--limit n]` | List memories. |
| `stats [--user-id id]` | Show statistics. |
| `set user <user_id>` | Set default user ID. |
| `set agent <agent_id>` | Set default agent ID. |
| `set json on\|off` | Enable/disable JSON output. |
| `show settings` | Show current session settings. |
| `clear` | Clear the screen. |
| `help` | Show help. |
| `exit`, `quit`, `q` | Exit the shell. |

**Example session:**

```bash
$ smem shell

==================================================
  SeekMem Interactive Mode
==================================================
Type 'help' for available commands, 'exit' to quit

seekmem> set user user123
seekmem> add "User prefers dark mode"
seekmem> search "preferences"
seekmem> list --limit 10
seekmem> exit
```

---

## Shell Completion

You can install tab-completion for `smem` (and `seekmem-cli`) so that subcommands and options are suggested on TAB.

**Install:**

```bash
# Bash
smem --install-completion bash
# Then source your ~/.bashrc or open a new terminal.

# Zsh
smem --install-completion zsh

# Fish
smem --install-completion fish

# PowerShell
smem --install-completion powershell
# Add the printed script to your $PROFILE to persist.
```

Bash/Zsh scripts are written under `~/.config/seekmem/` and, if you confirm, a source line is added to your `~/.bashrc` or `~/.zshrc`. Fish completion is installed under `~/.config/fish/completions/smem.fish`. PowerShell instructions are printed for you to add to your profile.

---

## Summary

- Use **`smem`** (or **`seekmem-cli`**) with **global options** (`-e`, `-j`, `-v`) and **subcommands** for memory, config, stats, manage, and shell.
- **Memory operations**: `memory add/search/get/update/delete/list/delete-all` with filters and JSON output.
- **Configuration**: `config show/validate/test/init` for inspecting, validating, testing, and interactively creating `.env`.
- **Statistics**: `stats` with optional user/agent filters and `--detailed`.
- **Management**: `manage backup/restore/cleanup/migrate` for backup, restore, retention cleanup, and store migration.
- **Interactive use**: `smem shell` for a REPL with session defaults and the same operations.
- **Completion**: `smem --install-completion bash|zsh|fish|powershell` for TAB completion.

For configuration details (e.g. `.env` variables), see the [Configuration Guide](./0003-configuration.md). For SDK and API usage, see [Getting Started](./0001-getting_started.md) and the [API documentation](../api/overview.md).
