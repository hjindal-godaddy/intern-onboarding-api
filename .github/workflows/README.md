# GitHub Actions Workflows

This directory contains CI/CD workflows for the Intern Onboarding API.

## Workflows

### 1. `ci-cd.yml` - Full CI/CD Pipeline
Complete pipeline that:
- Runs tests
- Builds Docker images
- Pushes to GitHub Container Registry
- Deploys to production (when on main branch)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### 2. `docker-build.yml` - Docker Build Only
Simpler workflow that:
- Builds Docker images
- Pushes to GitHub Container Registry

**Triggers:**
- Push to `main` branch
- Version tags (v*)
- Manual trigger (workflow_dispatch)

## Setup Instructions

### 1. Enable GitHub Actions
1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Enable "Allow all actions and reusable workflows"

### 2. GitHub Container Registry (GHCR)
The workflows automatically push to GitHub Container Registry:
- Images will be at: `ghcr.io/your-username/your-repo-name`
- No additional setup needed - uses `GITHUB_TOKEN` automatically

### 3. Secrets (Optional)
If you need additional secrets for deployment:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets like:
   - `OPENAI_API_KEY` (if needed in CI)
   - `DEPLOY_SSH_KEY` (for server deployment)
   - `SERVER_HOST` (deployment server address)

### 4. Environment Protection (Production)
For production deployments:

1. Go to **Settings** → **Environments**
2. Create "production" environment
3. Add required reviewers (optional)
4. Add environment secrets if needed

## Viewing Workflow Runs

1. Go to **Actions** tab in your GitHub repository
2. Click on a workflow run to see details
3. View logs, artifacts, and test results

## Customization

### Change Registry
Edit the `REGISTRY` and `IMAGE_NAME` env variables in workflow files.

### Add Deployment Steps
Edit the `deploy` job in `ci-cd.yml` to add your deployment commands.

### Add More Tests
Add test files in `tests/` directory - they'll run automatically.

## Troubleshooting

### Tests Failing
- Check MongoDB service is running in CI
- Verify test database connection
- Check test file syntax

### Docker Build Failing
- Verify Dockerfile.prod exists
- Check for syntax errors
- Ensure all dependencies are in requirements.txt

### Deployment Failing
- Verify deployment secrets are set
- Check server connectivity
- Verify deployment commands are correct
