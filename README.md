# Intern Onboarding API

![CI/CD](https://github.com/your-username/your-repo/actions/workflows/ci-cd.yml/badge.svg)

A FastAPI-based REST API for managing intern onboarding with features for intern profiles, task tracking, mentor assignment, and progress monitoring. Includes OpenAI integration for generating personalized welcome messages and document summarization.

## Features

- **Intern Management**: Create, read, update, and delete intern profiles
- **Task Tracking**: Manage onboarding tasks with status tracking
- **Mentor Assignment**: Assign mentors to interns
- **Progress Monitoring**: Track onboarding progress based on completed tasks
- **OpenAI Integration**: 
  - Generate personalized welcome messages
  - Summarize documents

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (using Motor async driver)
- **Validation**: Pydantic
- **AI**: OpenAI SDK

## Prerequisites

- Python 3.8+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key (optional, for AI features)

## Installation

1. Clone the repository:
```bash
cd new_intern_onboarding
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
# Or use: pip install -r requirements.txt (if pip points to Python 3)
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=intern_onboarding
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

### Option 1: Using Docker (Recommended)

**Development Mode:**

1. **Build and start all services** (MongoDB + API):
```bash
docker-compose up --build
```

2. **Run in detached mode** (background):
```bash
docker-compose up -d --build
```

3. **View logs**:
```bash
docker-compose logs -f
```

4. **Stop services**:
```bash
docker-compose down
```

5. **Stop and remove volumes** (clean slate):
```bash
docker-compose down -v
```

**Production Mode:**
```bash
# Build and start production environment
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

See [DOCKER.md](DOCKER.md) for detailed Docker documentation.

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Option 2: Local Development (without Docker)

1. **Set up MongoDB** (local or Atlas)
2. **Create `.env` file** with your MongoDB connection string
3. **Start the FastAPI server**:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Interns
- `POST /api/interns` - Create new intern
- `GET /api/interns` - List all interns
- `GET /api/interns/{id}` - Get intern details
- `PUT /api/interns/{id}` - Update intern
- `DELETE /api/interns/{id}` - Delete intern
- `POST /api/interns/{id}/welcome-message` - Generate welcome message
- `PUT /api/interns/{intern_id}/assign-mentor/{mentor_id}` - Assign mentor

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks` - List tasks (optional `intern_id` query param)
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Mark task as complete
- `DELETE /api/tasks/{id}` - Delete task

### Mentors
- `POST /api/mentors` - Create mentor
- `GET /api/mentors` - List all mentors
- `GET /api/mentors/{id}` - Get mentor details
- `PUT /api/mentors/{id}` - Update mentor
- `DELETE /api/mentors/{id}` - Delete mentor

### Progress
- `GET /api/interns/{id}/progress` - Get intern progress
- `POST /api/interns/{id}/progress/update` - Update progress

### OpenAI
- `POST /api/documents/summarize` - Summarize document

## Project Structure

```
new_intern_onboarding/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # MongoDB connection
│   ├── models.py               # MongoDB document models
│   ├── schemas.py              # Pydantic schemas
│   ├── routers/                # API route handlers
│   │   ├── interns.py
│   │   ├── tasks.py
│   │   ├── mentors.py
│   │   └── progress.py
│   ├── services/               # Business logic
│   │   ├── intern_service.py
│   │   ├── task_service.py
│   │   ├── mentor_service.py
│   │   └── openai_service.py
│   └── utils/
├── requirements.txt
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore               # Files to exclude from Docker build
├── .env.example
└── README.md
```

## Usage Examples

### Create an Intern
```bash
curl -X POST "http://localhost:8000/api/interns" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "start_date": "2024-01-15",
    "status": "active"
  }'
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "intern_id": "intern_id_here",
    "title": "Complete onboarding form",
    "description": "Fill out all required onboarding documents",
    "due_date": "2024-01-20"
  }'
```

### Generate Welcome Message
```bash
curl -X POST "http://localhost:8000/api/interns/{intern_id}/welcome-message" \
  -H "Content-Type: application/json"
```

## Docker Commands Reference

### Build and Start
```bash
docker-compose up --build
```

### Start in Background
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f mongodb
```

### Stop Services
```bash
docker-compose stop
```

### Remove Containers
```bash
docker-compose down
```

### Remove Containers and Volumes (clean slate)
```bash
docker-compose down -v
```

### Rebuild After Code Changes
```bash
docker-compose up --build
```

### Execute Commands in Container
```bash
# Access API container shell
docker-compose exec api bash

# Access MongoDB shell
docker-compose exec mongodb mongosh
```

## Environment Variables for Docker

When using Docker Compose, you can set environment variables in:
1. `.env` file (for OPENAI_API_KEY)
2. `docker-compose.yml` (already configured for MongoDB connection)

The MongoDB connection in Docker uses the service name `mongodb` instead of `localhost`.

## CI/CD

This project includes GitHub Actions workflows for:
- Automated testing
- Docker image building
- Container registry publishing
- Automated deployment

See [CI_CD.md](CI_CD.md) for detailed CI/CD setup instructions.

## License

MIT
