# Docker Setup Guide

This project is fully dockerized with separate configurations for development and production.

## Current Docker Setup

### Files
- `Dockerfile` - Development Docker image
- `Dockerfile.prod` - Production Docker image (optimized, multi-stage)
- `docker-compose.yml` - Development setup with hot-reload
- `docker-compose.prod.yml` - Production setup with health checks

## Development Mode

### Start Development Environment
```bash
docker-compose up --build
```

**Features:**
- Hot-reload enabled (code changes auto-refresh)
- Volume mounting for live code updates
- Debug mode enabled
- Single worker

### Stop Development Environment
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f api
docker-compose logs -f mongodb
```

## Production Mode

### Build Production Image
```bash
docker-compose -f docker-compose.prod.yml build
```

### Start Production Environment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Features:**
- Multi-stage build (smaller image size)
- 4 workers for better performance
- Health checks enabled
- No hot-reload (optimized)
- Non-root user for security
- Production optimizations

### Stop Production Environment
```bash
docker-compose -f docker-compose.prod.yml down
```

### Production Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

## Docker Commands Reference

### Development
```bash
# Start
docker-compose up --build

# Start in background
docker-compose up -d --build

# Stop
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild
docker-compose build --no-cache

# View logs
docker-compose logs -f api
```

### Production
```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Start
docker-compose -f docker-compose.prod.yml up -d

# Stop
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart
docker-compose -f docker-compose.prod.yml restart
```

## Image Sizes

- **Development**: ~500MB (includes build tools)
- **Production**: ~200MB (optimized, multi-stage build)

## Environment Variables

### Development (.env file)
```env
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=intern_onboarding
OPENAI_API_KEY=your_key_here
APP_NAME=Intern Onboarding API
DEBUG=True
```

### Production
Set environment variables in `docker-compose.prod.yml` or use `.env` file.

## Health Checks

Both development and production setups include health checks:
- API: `http://localhost:8000/health`
- MongoDB: Automatic ping check

## Data Persistence

- **Development**: `mongodb_data` volume
- **Production**: `mongodb_data_prod` volume

Data persists between container restarts.

## Troubleshooting

### Container won't start
```bash
docker-compose logs api
docker-compose logs mongodb
```

### Rebuild from scratch
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Check container status
```bash
docker-compose ps
```

### Access container shell
```bash
docker-compose exec api bash
docker-compose exec mongodb mongosh
```
