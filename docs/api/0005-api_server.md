# HTTP API Server

PowerMem HTTP API Server provides a production-ready RESTful API interface for PowerMem, enabling any application that supports HTTP calls to integrate PowerMem's intelligent memory capabilities.

## Overview

The PowerMem HTTP API Server is built with FastAPI and provides:

- **RESTful API endpoints** for all core PowerMem operations
- **API Key authentication** for secure access
- **Rate limiting** to protect server resources
- **Automatic API documentation** (Swagger UI and ReDoc)
- **Structured logging** with request tracking
- **CORS support** for web applications
- **Production-ready** deployment options

## Quick Start

### Installation

The API server is included with PowerMem. No additional installation is required.

### Starting the Server

#### Using the CLI Command

```bash
# Start server with default settings
powermem-server

# Start with custom host and port
powermem-server --host 0.0.0.0 --port 8000

# Start with auto-reload for development
powermem-server --reload

# Start with multiple workers
powermem-server --workers 4
```

#### Using Makefile

```bash
# Start server (production mode)
make server-start

# Start server with auto-reload (development mode)
make server-start-reload

# Check server status
make server-status

# View server logs
make server-logs

# Stop server
make server-stop

# Restart server
make server-restart
```

#### Using Uvicorn Directly

```bash
uvicorn powermem.server.main:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing the API

Once the server is running, you can access:

- **API Base URL**: `http://localhost:8000`
- **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`
- **Health Check**: `http://localhost:8000/api/v1/health`

## Configuration

### Environment Variables

The API server can be configured using environment variables. Create a `.env` file or set environment variables:

```bash
# Server Settings
POWERMEM_SERVER_HOST=0.0.0.0
POWERMEM_SERVER_PORT=8000
POWERMEM_SERVER_WORKERS=4
POWERMEM_SERVER_RELOAD=false

# Authentication
POWERMEM_AUTH_ENABLED=true
POWERMEM_API_KEYS=your_key_1,your_key_2,your_key_3

# Rate Limiting
POWERMEM_RATE_LIMIT_ENABLED=true
POWERMEM_RATE_LIMIT_PER_MINUTE=100

# Logging
POWERMEM_LOG_LEVEL=INFO
POWERMEM_LOG_FORMAT=json

# API Settings
POWERMEM_API_TITLE=PowerMem API
POWERMEM_API_VERSION=v1
POWERMEM_API_DESCRIPTION=PowerMem HTTP API Server - Intelligent Memory System

# CORS
POWERMEM_CORS_ENABLED=true
POWERMEM_CORS_ORIGINS=*
```

See `.env.example` for a complete list of configuration options.

## Authentication

### API Key Authentication

By default, the API server requires API key authentication. You can provide the API key in two ways:

#### Header Method (Recommended)

```bash
curl -H "X-API-Key: your_api_key" http://localhost:8000/api/v1/health
```

#### Query Parameter Method

```bash
curl http://localhost:8000/api/v1/health?api_key=your_api_key
```

### Disabling Authentication

For development, you can disable authentication by setting:

```bash
POWERMEM_AUTH_ENABLED=false
```

**Warning**: Never disable authentication in production environments.

## API Endpoints

### Memory Management

#### Create Memory

```http
POST /api/v1/memories
Content-Type: application/json
X-API-Key: your_api_key

{
  "content": "User likes coffee",
  "user_id": "user123",
  "agent_id": "agent001",
  "metadata": {
    "source": "conversation",
    "timestamp": "2025-01-01T00:00:00Z"
  },
  "scope": "user",
  "memory_type": "preference",
  "infer": true
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "memory_id": 1,
    "content": "User likes coffee",
    "user_id": "user123",
    "agent_id": "agent001",
    "metadata": {},
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  },
  "message": "Memory created successfully",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

#### Batch Create Memories

Create multiple memories in a single request:

```http
POST /api/v1/memories/batch
Content-Type: application/json
X-API-Key: your_api_key

{
  "memories": [
    {
      "content": "User likes coffee",
      "metadata": {"source": "conversation"},
      "memory_type": "preference"
    },
    {
      "content": "User works as a software engineer",
      "metadata": {"source": "profile"},
      "memory_type": "background"
    },
    {
      "content": "User prefers Python over Java",
      "metadata": {"source": "conversation"},
      "memory_type": "preference"
    }
  ],
  "user_id": "user123",
  "agent_id": "agent001",
  "infer": true
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "memories": [
      {
        "memory_id": 1,
        "content": "User likes coffee",
        "user_id": "user123",
        "metadata": {},
        "created_at": "2025-01-01T00:00:00Z"
      },
      {
        "memory_id": 2,
        "content": "User works as a software engineer",
        "user_id": "user123",
        "metadata": {},
        "created_at": "2025-01-01T00:00:00Z"
      },
      {
        "memory_id": 3,
        "content": "User prefers Python over Java",
        "user_id": "user123",
        "metadata": {},
        "created_at": "2025-01-01T00:00:00Z"
      }
    ],
    "total": 3,
    "created_count": 3,
    "failed_count": 0,
    "failed": []
  },
  "message": "Created 3 out of 3 memories",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

**Note**: Batch creation supports up to 100 memories per request. If some memories fail to create, they will be listed in the `failed` array with error details.

#### List Memories

```http
GET /api/v1/memories?user_id=user123&limit=10&offset=0
X-API-Key: your_api_key
```

#### Get Memory

```http
GET /api/v1/memories/{memory_id}
X-API-Key: your_api_key
```

#### Update Memory

```http
PUT /api/v1/memories/{memory_id}
Content-Type: application/json
X-API-Key: your_api_key

{
  "content": "User loves coffee",
  "metadata": {
    "updated": true
  }
}
```

#### Delete Memory

```http
DELETE /api/v1/memories/{memory_id}
X-API-Key: your_api_key
```

#### Bulk Delete Memories

```http
DELETE /api/v1/memories
Content-Type: application/json
X-API-Key: your_api_key

{
  "memory_ids": [1, 2, 3],
  "user_id": "user123"
}
```

### Memory Search

#### Search Memories (POST)

```http
POST /api/v1/memories/search
Content-Type: application/json
X-API-Key: your_api_key

{
  "query": "user preferences",
  "user_id": "user123",
  "limit": 10,
  "filters": {
    "memory_type": "preference"
  }
}
```

#### Search Memories (GET)

```http
GET /api/v1/memories/search?query=user%20preferences&user_id=user123&limit=10
X-API-Key: your_api_key
```

**Response:**

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "memory_id": 1,
        "content": "User likes coffee",
        "score": 0.95,
        "metadata": {}
      }
    ],
    "total": 1,
    "query": "user preferences"
  },
  "message": "Search completed successfully",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

### User Profile Management

#### Get User Profile

```http
GET /api/v1/users/{user_id}/profile
X-API-Key: your_api_key
```

#### Update User Profile

```http
POST /api/v1/users/{user_id}/profile
Content-Type: application/json
X-API-Key: your_api_key

{
  "profile_content": "User is a software engineer who loves Python",
  "topics": {
    "profession": "software_engineer",
    "interests": ["python", "ai", "machine_learning"]
  }
}
```

#### Get User Memories

```http
GET /api/v1/users/{user_id}/memories?limit=100&offset=0
X-API-Key: your_api_key
```

### Agent Memory Management

#### Get Agent Memories

```http
GET /api/v1/agents/{agent_id}/memories?limit=100&offset=0
X-API-Key: your_api_key
```

#### Create Agent Memory

```http
POST /api/v1/agents/{agent_id}/memories?content=Agent%20learned%20something
X-API-Key: your_api_key
```

#### Share Memories Between Agents

```http
POST /api/v1/agents/{agent_id}/memories/share
Content-Type: application/json
X-API-Key: your_api_key

{
  "target_agent_id": "agent002",
  "memory_ids": [1, 2, 3]
}
```

#### Get Shared Memories

```http
GET /api/v1/agents/{agent_id}/memories/shared?limit=100&offset=0
X-API-Key: your_api_key
```

### System Management

#### Health Check

```http
GET /api/v1/health
```

**Response:**

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-01-01T00:00:00Z"
  },
  "message": "Service is healthy",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

#### System Status

```http
GET /api/v1/status
X-API-Key: your_api_key
```

**Response:**

```json
{
  "success": true,
  "data": {
    "status": "operational",
    "version": "v1",
    "storage_type": "oceanbase",
    "llm_provider": "qwen",
    "timestamp": "2025-01-01T00:00:00Z"
  },
  "message": "System status retrieved successfully",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

#### Metrics (Prometheus Format)

```http
GET /api/v1/metrics
X-API-Key: your_api_key
```

#### Reset All Memories

```http
POST /api/v1/reset
X-API-Key: your_api_key
```

**Warning**: This endpoint deletes all memories. Use with caution.

## Error Handling

The API uses a standardized error response format:

```json
{
  "success": false,
  "error": {
    "code": "MEMORY_NOT_FOUND",
    "message": "Memory 123 not found",
    "details": {}
  },
  "timestamp": "2025-01-01T00:00:00Z"
}
```

### Common Error Codes

- `UNAUTHORIZED` - Missing or invalid API key
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `INVALID_REQUEST` - Invalid request parameters
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `MEMORY_NOT_FOUND` - Memory does not exist
- `MEMORY_CREATE_FAILED` - Failed to create memory
- `SEARCH_FAILED` - Search operation failed
- `INTERNAL_ERROR` - Internal server error

## Rate Limiting

The API server implements rate limiting to protect server resources. By default, each IP address is limited to 100 requests per minute.

When rate limit is exceeded, the API returns:

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded: 100 per 1 minute",
    "details": {}
  },
  "timestamp": "2025-01-01T00:00:00Z"
}
```

You can configure rate limits using:

```bash
POWERMEM_RATE_LIMIT_ENABLED=true
POWERMEM_RATE_LIMIT_PER_MINUTE=100
```

## Code Examples

### Python

```python
import requests

API_BASE = "http://localhost:8000/api/v1"
API_KEY = "your_api_key"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Create a memory
response = requests.post(
    f"{API_BASE}/memories",
    headers=headers,
    json={
        "content": "User likes Python programming",
        "user_id": "user123"
    }
)
print(response.json())

# Batch create memories
response = requests.post(
    f"{API_BASE}/memories/batch",
    headers=headers,
    json={
        "memories": [
            {"content": "User likes Python programming"},
            {"content": "User works as a software engineer"},
            {"content": "User prefers coffee over tea"}
        ],
        "user_id": "user123"
    }
)
result = response.json()
print(f"Created {result['data']['created_count']} memories")
print(f"Failed {result['data']['failed_count']} memories")

# Search memories
response = requests.post(
    f"{API_BASE}/memories/search",
    headers=headers,
    json={
        "query": "programming preferences",
        "user_id": "user123",
        "limit": 10
    }
)
print(response.json())
```

### JavaScript/TypeScript

```typescript
const API_BASE = 'http://localhost:8000/api/v1';
const API_KEY = 'your_api_key';

const headers = {
  'X-API-Key': API_KEY,
  'Content-Type': 'application/json'
};

// Create a memory
const createMemory = async () => {
  const response = await fetch(`${API_BASE}/memories`, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({
      content: 'User likes TypeScript programming',
      user_id: 'user123'
    })
  });
  return response.json();
};

// Search memories
const searchMemories = async () => {
  const response = await fetch(`${API_BASE}/memories/search`, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({
      query: 'programming preferences',
      user_id: 'user123',
      limit: 10
    })
  });
  return response.json();
};
```

### cURL

```bash
# Create memory
curl -X POST http://localhost:8000/api/v1/memories \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User likes coffee",
    "user_id": "user123"
  }'

# Search memories
curl -X POST http://localhost:8000/api/v1/memories/search \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "user preferences",
    "user_id": "user123",
    "limit": 10
  }'

# Get memory
curl -X GET http://localhost:8000/api/v1/memories/1 \
  -H "X-API-Key: your_api_key"
```

## Deployment

### Development

For development, use auto-reload mode:

```bash
powermem-server --reload
```

### Production

For production deployment, use multiple workers:

```bash
powermem-server --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -e ".[server]"

EXPOSE 8000
CMD ["powermem-server", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Build and run:

```bash
docker build -t powermem-server .
docker run -p 8000:8000 powermem-server
```

### Kubernetes

The API server supports Kubernetes deployment with:

- Health check endpoints (`/api/v1/health`)
- Readiness probes
- Liveness probes
- Horizontal scaling

Example deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: powermem-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: powermem-server
  template:
    metadata:
      labels:
        app: powermem-server
    spec:
      containers:
      - name: powermem-server
        image: powermem-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: POWERMEM_SERVER_HOST
          value: "0.0.0.0"
        - name: POWERMEM_SERVER_PORT
          value: "8000"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Monitoring and Logging

### Logging

The server supports structured logging in JSON format:

```bash
POWERMEM_LOG_FORMAT=json
POWERMEM_LOG_LEVEL=INFO
```

Logs include:
- Request ID for tracing
- Timestamp
- Request method and path
- Response status code
- Duration
- Error details (if any)

### Metrics

Access Prometheus-format metrics at `/api/v1/metrics`:

```bash
curl http://localhost:8000/api/v1/metrics -H "X-API-Key: your_api_key"
```

## Best Practices

1. **Always use HTTPS in production** - The API server should be behind a reverse proxy (nginx, Traefik) with TLS termination.

2. **Use environment variables for configuration** - Never hardcode API keys or sensitive configuration.

3. **Implement proper error handling** - Check response status codes and handle errors appropriately.

4. **Use connection pooling** - For high-traffic applications, use HTTP connection pooling.

5. **Monitor rate limits** - Be aware of rate limits and implement exponential backoff for retries.

6. **Cache responses when appropriate** - Cache frequently accessed data to reduce API calls.

7. **Use pagination** - Always use pagination for list endpoints to avoid loading too much data.

## Troubleshooting

### Server Won't Start

- Check if the port is already in use: `lsof -i :8000`
- Verify configuration in `.env` file
- Check logs: `make server-logs` or `tail -f server.log`

### Authentication Errors

- Verify API key is set correctly: `POWERMEM_API_KEYS=your_key`
- Check if authentication is enabled: `POWERMEM_AUTH_ENABLED=true`
- Ensure API key is included in request headers

### Rate Limit Errors

- Increase rate limit: `POWERMEM_RATE_LIMIT_PER_MINUTE=200`
- Disable rate limiting for development: `POWERMEM_RATE_LIMIT_ENABLED=false`

### Connection Errors

- Verify server is running: `make server-status`
- Check firewall settings
- Ensure correct host and port configuration

## API Versioning

The API uses path-based versioning. Current version is `v1`:

- Current: `/api/v1/...`
- Future versions: `/api/v2/...`, `/api/v3/...`

Multiple API versions can coexist, allowing gradual migration.

## Support

For issues, questions, or contributions:

- **GitHub Issues**: [https://github.com/powermem/powermem/issues](https://github.com/powermem/powermem/issues)
- **Documentation**: [https://powermem.readthedocs.io](https://powermem.readthedocs.io)

## See Also

- [Memory API](./0001-memory.md) - Python SDK memory operations
- [AsyncMemory API](./0002-async_memory.md) - Asynchronous memory operations
- [Agent APIs](./0003-agents.md) - Multi-agent memory management
- [Configuration Guide](../guides/0003-configuration.md) - PowerMem configuration
