# 🚀 TITAN QUICKSTART

> **Goal**: Get Titan running in 5 minutes

## Prerequisites

- Docker & Docker Compose installed
- 16GB+ RAM
- 20GB+ free disk space

## Quick Start (3 commands)

```bash
# 1. Bootstrap the environment
./automation/setup/bootstrap.sh

# 2. Start services
docker-compose up -d

# 3. Check status
docker-compose ps
```

**Done!** Connect with Minecraft client to `localhost:25565`

## Even Faster (with Make)

```bash
make bootstrap
make start
```

## Verify Everything Works

```bash
# Check service health
./automation/monitoring/health-check.sh

# View logs
docker-compose logs -f titan-proxy

# Open monitoring dashboard
# Browser: http://localhost:3000 (Grafana, admin/admin)
```

## Common Commands

| Command | What it does |
|---------|-------------|
| `make start` | Start all services |
| `make stop` | Stop all services |
| `make restart` | Restart everything |
| `make logs` | View all logs |
| `make status` | Check health |
| `make deploy` | Build & deploy |
| `make ship` | Full build, test, deploy |

## Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# Check ports aren't in use
netstat -an | grep 25565

# View error logs
docker-compose logs
```

### Can't connect to server
```bash
# Check if proxy is running
docker-compose ps titan-proxy

# Check proxy logs
docker-compose logs titan-proxy

# Test connectivity
nc -zv localhost 25565
```

### Database connection failed
```bash
# Check PostgreSQL
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U titan -c "SELECT 1;"
```

## What's Running?

| Service | Port | URL/Connection |
|---------|------|----------------|
| Minecraft Server | 25565 | `localhost:25565` |
| Grafana (Monitoring) | 3000 | `http://localhost:3000` |
| Prometheus (Metrics) | 9090 | `http://localhost:9090` |
| PostgreSQL | 5432 | `localhost:5432` |
| Redis | 6379 | `localhost:6379` |

## Next Steps

1. **Read Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. **Customize Config**: Edit `.env` file
3. **Add Plugins**: Put JARs in `plugins/` folder
4. **Scale Up**: See [docs/SCALING.md](docs/SCALING.md)
5. **Deploy Production**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Development

```bash
# Build from source
./gradlew build

# Run tests
./gradlew test

# Hot reload (rebuild and restart)
make deploy
```

## Getting Help

- **Logs**: `docker-compose logs -f`
- **Health**: `./automation/monitoring/health-check.sh`
- **Issues**: [GitHub Issues](https://github.com/yourusername/project-mc-serv-mc.galion.studio/issues)
- **Docs**: [docs/](docs/)

---

**Built with Elon Musk principles**: Ship fast. Iterate fast. Build amazing things. 🚀

