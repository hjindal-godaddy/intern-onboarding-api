# CI/CD Setup Guide

This project uses GitHub Actions for continuous integration and continuous deployment.

## Overview

The CI/CD pipeline includes:
- ✅ Automated testing
- ✅ Code linting
- ✅ Docker image building
- ✅ Container registry publishing
- ✅ Automated deployment (optional)

## Workflows

### 1. Full CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Steps:**
1. **Test Job**
   - Sets up Python 3.9
   - Starts MongoDB service
   - Installs dependencies
   - Runs linting (flake8)
   - Runs tests (pytest)
   - Uploads coverage reports

2. **Build Job** (only on push)
   - Builds Docker image using `Dockerfile.prod`
   - Pushes to GitHub Container Registry
   - Tags images with branch, SHA, and version

3. **Deploy Job** (only on main branch)
   - Deploys to production environment
   - Customize this step for your deployment needs

### 2. Docker Build Only (`docker-build.yml`)

**Triggers:**
- Push to `main` branch
- Version tags (e.g., `v1.0.0`)
- Manual trigger

**Steps:**
- Builds and pushes Docker image to GHCR

## Setup Steps

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit with CI/CD"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### Step 2: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

### Step 3: View Workflow Runs

1. Go to **Actions** tab in your repository
2. You'll see workflows running automatically
3. Click on a run to see detailed logs

## Container Registry

Images are automatically pushed to:
```
ghcr.io/your-username/your-repo-name:latest
ghcr.io/your-username/your-repo-name:main-abc1234
```

### Pulling Images

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/your-username/your-repo-name:latest
```

## Customization

### Add Deployment Steps

Edit `.github/workflows/ci-cd.yml`:

```yaml
- name: Deploy to server
  run: |
    ssh user@server "cd /app && \
      docker pull ghcr.io/your-username/your-repo-name:latest && \
      docker-compose up -d"
```

### Add Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets like:
   - `OPENAI_API_KEY`
   - `DEPLOY_SSH_KEY`
   - `SERVER_HOST`

Then use in workflow:
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Change Test Commands

Edit the `test` job in `ci-cd.yml`:

```yaml
- name: Run custom tests
  run: |
    pytest tests/ -v --cov=app
```

## Testing Locally

### Run Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html
```

### Run Linting

```bash
pip install flake8 black
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Workflow Status Badge

Add to your README.md:

```markdown
![CI/CD](https://github.com/your-username/your-repo/actions/workflows/ci-cd.yml/badge.svg)
```

## Troubleshooting

### Tests Fail in CI

- Check MongoDB service is running
- Verify test database connection string
- Check test file syntax

### Docker Build Fails

- Verify `Dockerfile.prod` exists
- Check for syntax errors
- Ensure all dependencies in `requirements.txt`

### Images Not Pushing

- Check GitHub Actions permissions
- Verify `GITHUB_TOKEN` has package write access
- Check workflow logs for errors

### Deployment Fails

- Verify deployment secrets are set
- Check server connectivity
- Verify deployment commands are correct
- Check environment protection rules

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Enable GitHub Actions
3. ✅ Watch workflows run
4. ✅ Customize deployment steps
5. ✅ Set up production environment

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
