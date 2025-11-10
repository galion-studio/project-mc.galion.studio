# 🚀 TITAN DEPLOYMENT GUIDE

> **SHIP IT NOW** - Quick deployment instructions

## Quick Deploy (5 minutes)

### Windows

```powershell
# 1. Open PowerShell in project directory
cd C:\Users\Gigabyte\Documents\project-mc-serv-mc.galion.studio

# 2. Start services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f
```

### Linux/Mac

```bash
# 1. Navigate to project
cd /path/to/project-mc-serv-mc.galion.studio

# 2. Bootstrap (first time only)
chmod +x automation/setup/bootstrap.sh
./automation/setup/bootstrap.sh

# 3. Start services
docker-compose up -d

# Or use Make
make start
```

## What Gets Deployed

✅ **Titan Proxy** - Player router (port 25565)  
✅ **Hub Server** - Lobby server  
✅ **Survival Server** - Game server  
✅ **PostgreSQL** - Database (port 5432)  
✅ **Redis** - Cache (port 6379)  
✅ **Prometheus** - Metrics (port 9090)  
✅ **Grafana** - Dashboards (port 3000)

## Connect & Test

```
Minecraft Client: localhost:25565
Grafana Dashboard: http://localhost:3000 (admin/admin)
Prometheus: http://localhost:9090
```

## Verify Deployment

### Check Services
```bash
docker-compose ps
```

Expected output: All services "Up" and "healthy"

### Check Logs
```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs titan-proxy
docker-compose logs titan-survival
```

### Health Check
```bash
# Linux/Mac
./automation/monitoring/health-check.sh

# Windows
docker-compose exec titan-proxy nc -zv localhost 25577
```

## Common Issues & Fixes

### Port Already in Use
```bash
# Check what's using port 25565
netstat -ano | findstr :25565  # Windows
lsof -i :25565                  # Linux/Mac

# Kill the process or change port in .env
```

### Services Won't Start
```bash
# Check Docker is running
docker ps

# Check logs for errors
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d --build
```

### Can't Connect to Server
```bash
# Check proxy is running
docker-compose ps titan-proxy

# Check proxy logs
docker-compose logs titan-proxy

# Test connectivity
nc -zv localhost 25565
```

## Production Deployment

For production deployment, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

Key differences:
- Use Kubernetes instead of Docker Compose
- Set up load balancers
- Configure auto-scaling
- Enable monitoring & alerts
- Set up backups
- Harden security

## Rapid Iteration

### Quick Redeploy
```bash
# Build and restart
docker-compose down
docker-compose up -d --build

# Or use Make
make deploy
```

### Update Code
```bash
# Pull changes
git pull

# Rebuild
./gradlew build

# Redeploy
docker-compose up -d --build
```

### View Metrics
```bash
# Open Grafana
open http://localhost:3000  # Mac
start http://localhost:3000 # Windows
```

## Scaling

### Add More Game Servers
```bash
# Scale survival servers to 3 instances
docker-compose up -d --scale titan-survival=3

# Scale hub servers
docker-compose up -d --scale titan-hub=2
```

### Resource Limits
Edit `docker-compose.yml`:
```yaml
titan-survival:
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 16G
```

## Backup

```bash
# Create backup
./automation/backup/backup.sh

# Backups saved to: /backups/
```

## Stop Everything

```bash
# Stop services (keep data)
docker-compose down

# Stop and remove volumes (DESTROYS DATA)
docker-compose down -v

# Or use Make
make stop
```

## Monitoring

### View Logs
```bash
make logs            # All logs
make logs-proxy      # Proxy logs
make logs-survival   # Survival logs
```

### Check Health
```bash
make status
```

### View Metrics
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Next Steps

1. **Customize Configuration** - Edit `.env` file
2. **Add Plugins** - Put JARs in `plugins/` folder
3. **Configure Worlds** - Edit `worlds/` directory
4. **Scale Up** - Add more servers
5. **Go Production** - Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## ELON MODE: One Command Deploy

```bash
# Everything in one command
git clone <repo> && cd <repo> && ./automation/setup/bootstrap.sh && docker-compose up -d
```

**DONE. SHIPPED. ITERATE.**

---

**Built to ship fast. Built to scale. Built for 20k players.** 🚀

