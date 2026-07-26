# HomeOps

HomeOps is a Python-based homelab control plane for monitoring infrastructure and managing approved services.

The project integrates with Prometheus and Docker to provide infrastructure status, container visibility, and operational controls through a terminal interface and, later, a Telegram bot.

## Current Features

- Prometheus API integration
- Infrastructure target status checks
- Structured terminal output using Rich
- Environment-based configuration
- Git-based development workflow

## Planned Features

- Docker container status
- Approved container restart commands
- Recent container log retrieval
- Telegram command interface
- CPU and memory summaries
- Backup status checks
- Security status reporting
- Action logging
- Automated tests

## Architecture

```text
Terminal / Telegram
        |
        v
     HomeOps
        |
   +----+----+
   |         |
Prometheus  Docker
   |         |
Metrics   Containers
