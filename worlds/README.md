# Titan Worlds Directory

This directory contains all Minecraft world data for Titan servers.

## Structure

```
worlds/
├── hub/         - Lobby/Hub world
├── survival/    - Survival game world
├── creative/    - Creative world (optional)
└── minigames/   - Minigame worlds (optional)
```

## Important Notes

⚠️ **World files are NOT included in git** (too large)

World data is stored in Docker volumes and/or this directory depending on your configuration.

## Backup Your Worlds

Always backup your worlds regularly:

```bash
# Manual backup
./automation/backup/backup.sh

# Automated backups run every 6 hours (if configured)
```

## Importing Existing Worlds

To import an existing Minecraft world:

1. Stop the server:
   ```bash
   docker-compose down
   ```

2. Copy your world folder here:
   ```bash
   cp -r /path/to/your/world worlds/survival/
   ```

3. Ensure proper permissions:
   ```bash
   chmod -R 755 worlds/survival/
   ```

4. Start the server:
   ```bash
   docker-compose up -d
   ```

## World Configuration

World settings are configured in:
- `config/server.yml` - Titan server configuration
- `docker/config/server.properties.template` - Minecraft server properties

## Performance Tips

For best performance with high player counts:

1. **Pre-generate chunks**: Use Chunky or similar plugin
2. **Optimize world border**: Set reasonable world border size
3. **Limit world size**: Smaller worlds = better performance
4. **Regular maintenance**: Trim unused chunks periodically

## Hub World Recommendations

The hub/lobby world should be:
- Small (200x200 blocks recommended)
- Flat terrain (reduces lag)
- Minimal entities (no mobs, limited animals)
- Pre-built spawn area
- No complex redstone

## Game World Recommendations

For survival/game worlds:
- Pre-generate spawn area (500 block radius minimum)
- Set world border (10,000 blocks recommended for testing)
- Disable auto-save during high-load periods
- Use Paper's async chunk loading (enabled by default)

## Troubleshooting

### World Not Loading
- Check file permissions
- Verify world folder name matches configuration
- Check Docker volume mounts in docker-compose.yml

### Corrupted World
- Restore from backup
- Use Minecraft's built-in world repair tools
- Check server logs for errors

### Performance Issues
- Pre-generate chunks
- Reduce view distance
- Limit entity counts
- Optimize spawn rates

---

**For more information, see [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)**

