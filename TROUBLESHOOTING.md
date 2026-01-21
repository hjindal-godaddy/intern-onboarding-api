# Troubleshooting Guide

## Browser Can't Open the Page

### Step 1: Check if Docker is Running
```bash
docker ps
```
If this fails, start Docker Desktop.

### Step 2: Check if Containers are Running
```bash
cd /Users/hjindal/Desktop/new_intern_onboarding
docker-compose ps
```

You should see both `intern_onboarding_api` and `intern_onboarding_mongodb` with status "Up".

### Step 3: Check Container Logs
```bash
# Check API logs
docker-compose logs api

# Check MongoDB logs
docker-compose logs mongodb

# Follow logs in real-time
docker-compose logs -f api
```

### Step 4: Check if Port 8000 is in Use
```bash
lsof -i :8000
```
If something is using port 8000, either:
- Stop that service, or
- Change the port in `docker-compose.yml` (e.g., "8001:8000")

### Step 5: Restart Containers
```bash
docker-compose down
docker-compose up --build
```

### Step 6: Check Container Health
```bash
# Check if API container is responding
docker-compose exec api curl http://localhost:8000/health

# Or from your host machine
curl http://localhost:8000/health
```

### Step 7: Common Issues

#### Issue: "Connection refused"
- **Solution**: Containers might not be running. Run `docker-compose up`

#### Issue: "Cannot connect to MongoDB"
- **Solution**: Wait a few seconds for MongoDB to fully start, then restart API:
  ```bash
  docker-compose restart api
  ```

#### Issue: Port already in use
- **Solution**: Change port in `docker-compose.yml`:
  ```yaml
  ports:
    - "8001:8000"  # Use 8001 instead of 8000
  ```

#### Issue: Permission denied
- **Solution**: Make sure Docker Desktop is running and you have permissions

### Step 8: Verify from Terminal
```bash
# Test if API is responding
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### Step 9: Check Browser
- Try: `http://127.0.0.1:8000/docs` instead of `localhost`
- Try: `http://localhost:8000/health` first
- Clear browser cache
- Try incognito/private mode
- Try a different browser

### Step 10: Full Reset
If nothing works, do a complete reset:
```bash
docker-compose down -v
docker-compose up --build
```
