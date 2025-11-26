# Deployment Guide

## Quick Overview

| Method | Difficulty | Use Case |
|--------|------------|----------|
| **HTTP/SSE Server** | ⭐ Easy | Remote access, cloud deployment |
| **Docker** | ⭐⭐ Medium | Containers, microservices |
| **Systemd** | ⭐⭐ Medium | Linux servers, always-on service |
| **Stdio (Local)** | ⭐ Easy | Local development, Cursor/Claude Desktop |

---

## 1. HTTP/SSE Server (Recommended for Production)

Deploy server accessible via HTTP/SSE transport for remote access.

### Basic HTTP/SSE Server

```bash
cd /Users/laptop/dev/r2r-fastmcp/mcp-server

# Run with HTTP/SSE transport
python server_ultra.py --transport sse --port 8000

# Or with fastmcp CLI
fastmcp run server_ultra.py --transport sse --port 8000
```

### Production HTTP Server

Create `run_server.py`:

```python
#!/usr/bin/env python3
from server_ultra import mcp

if __name__ == "__main__":
    # Run with SSE transport on all interfaces
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

Run it:

```bash
python run_server.py
```

Access at: `http://your-server:8000/sse`

### Connect from Cursor

```json
{
  "mcpServers": {
    "r2r-http": {
      "url": "http://your-server:8000/sse",
      "transport": "sse"
    }
  }
}
```

---

## 2. Docker Deployment

Deploy using Docker for containerization.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt pyproject.toml ./
COPY server_ultra.py ./
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Environment variables
ENV R2R_BASE_URL=${R2R_BASE_URL:-http://localhost:7272}
ENV API_KEY=${API_KEY}

# Run server
CMD ["python", "server_ultra.py", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build
docker build -t r2r-mcp-server .

# Run
docker run -d \
  --name r2r-mcp \
  -p 8000:8000 \
  -e R2R_BASE_URL=http://your-r2r:7272 \
  -e API_KEY=your_key \
  r2r-mcp-server

# View logs
docker logs -f r2r-mcp

# Stop
docker stop r2r-mcp
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  r2r-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - R2R_BASE_URL=${R2R_BASE_URL}
      - API_KEY=${API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run:

```bash
docker-compose up -d
```

---

## 3. Systemd Service (Linux)

Deploy as a systemd service for automatic startup.

### Create Service File

`/etc/systemd/system/r2r-mcp.service`:

```ini
[Unit]
Description=R2R Ultra MCP Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/r2r-mcp
Environment="R2R_BASE_URL=http://localhost:7272"
Environment="API_KEY=your_key_here"
ExecStart=/usr/bin/python3 /opt/r2r-mcp/server_ultra.py --transport sse --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Install and Start

```bash
# Copy files
sudo cp server_ultra.py /opt/r2r-mcp/

# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable r2r-mcp

# Start service
sudo systemctl start r2r-mcp

# Check status
sudo systemctl status r2r-mcp

# View logs
sudo journalctl -u r2r-mcp -f
```

---

## 4. Nginx Reverse Proxy (Optional)

Add SSL and domain name using Nginx.

### Nginx Configuration

`/etc/nginx/sites-available/r2r-mcp`:

```nginx
server {
    listen 80;
    server_name mcp.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mcp.yourdomain.com;

    # SSL certificates (use certbot)
    ssl_certificate /etc/letsencrypt/live/mcp.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mcp.yourdomain.com/privkey.pem;

    # Proxy to MCP server
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # SSE specific
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/r2r-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Get SSL certificate:

```bash
sudo certbot --nginx -d mcp.yourdomain.com
```

---

## 5. Environment Variables

### Production Best Practices

**Option 1: .env file**

```bash
# /opt/r2r-mcp/.env
R2R_BASE_URL=https://your-r2r-instance.com
API_KEY=your_secret_key_here
MAX_RETRIES=3
TIMEOUT=120.0
```

Load in service:

```ini
[Service]
EnvironmentFile=/opt/r2r-mcp/.env
```

**Option 2: systemd environment**

```bash
# Create environment file
sudo mkdir -p /etc/r2r-mcp
sudo nano /etc/r2r-mcp/environment

# Add variables
R2R_BASE_URL=https://your-r2r-instance.com
API_KEY=your_secret_key

# Reference in service
[Service]
EnvironmentFile=/etc/r2r-mcp/environment
```

---

## 6. Monitoring

### Check Server Status

```bash
# Via HTTP endpoint
curl http://localhost:8000/health

# Via MCP tool (if using client)
from fastmcp import Client

async with Client("http://localhost:8000/sse") as client:
    result = await client.call_tool("get_server_capabilities", {})
    print(result)
```

### Monitor Logs

**Systemd:**
```bash
# Real-time logs
sudo journalctl -u r2r-mcp -f

# Search for errors
sudo journalctl -u r2r-mcp | grep ERROR

# Last 100 lines
sudo journalctl -u r2r-mcp -n 100
```

**Docker:**
```bash
# Real-time logs
docker logs -f r2r-mcp

# Search for errors
docker logs r2r-mcp 2>&1 | grep ERROR
```

### Performance Statistics

Call `get_performance_stats()` tool:

```python
from fastmcp import Client

async with Client("http://localhost:8000/sse") as client:
    stats = await client.call_tool("get_performance_stats", {})
    print(f"Cache hit rate: {stats['cache']['hit_rate']}")
    print(f"Total requests: {stats['timing']['total_calls']}")
```

---

## 7. Security Best Practices

### 1. Use HTTPS

Always use SSL/TLS for production (Nginx + Let's Encrypt).

### 2. Firewall Configuration

```bash
# Allow only from specific IPs
sudo ufw allow from 192.168.1.0/24 to any port 8000

# Or use Nginx as gateway
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 8000/tcp
```

### 3. API Key Management

```bash
# Never commit API keys
# Use environment variables or secret management

# Generate strong key
openssl rand -base64 32
```

### 4. Rate Limiting

server_ultra.py has built-in rate limiting (100 req/min default).

To adjust:

```python
# In server_ultra.py
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=1000))
```

---

## 8. Updates and Maintenance

### Zero-Downtime Update

**With Systemd:**

```bash
# Pull latest code
cd /opt/r2r-mcp
git pull

# Reload service (systemd handles graceful restart)
sudo systemctl reload r2r-mcp
```

**With Docker:**

```bash
# Build new image
docker build -t r2r-mcp-server:latest .

# Stop old container
docker stop r2r-mcp

# Remove old container
docker rm r2r-mcp

# Start new container
docker run -d --name r2r-mcp -p 8000:8000 \
  -e R2R_BASE_URL=$R2R_BASE_URL \
  -e API_KEY=$API_KEY \
  r2r-mcp-server:latest
```

### Rollback

**Git:**

```bash
cd /opt/r2r-mcp
git checkout HEAD~1  # Go back one commit
sudo systemctl restart r2r-mcp
```

**Docker:**

```bash
docker run -d --name r2r-mcp r2r-mcp-server:previous-tag
```

---

## 9. Troubleshooting

### Server Won't Start

```bash
# Check Python version
python3 --version  # Needs 3.10+

# Check dependencies
pip list | grep fastmcp

# Check environment variables
env | grep R2R
```

### Connection Refused

```bash
# Check if running
ps aux | grep server_ultra

# Check port
netstat -tulpn | grep 8000

# Check firewall
sudo ufw status
```

### High Memory Usage

```bash
# Check process
top -p $(pgrep -f server_ultra)

# Restart service
sudo systemctl restart r2r-mcp
```

### Cache Issues

```python
# Clear cache via tool
async with Client("http://localhost:8000/sse") as client:
    result = await client.call_tool("clear_cache", {})
```

---

## Summary

- **Development**: Use stdio transport (localhost only)
- **Small team**: HTTP/SSE on internal network
- **Production**: Docker + Nginx + SSL
- **Enterprise**: Kubernetes with multiple replicas

For more help, see `ULTRA_README.md` for server_ultra.py features.

