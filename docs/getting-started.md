# Getting Started

This guide will help you set up the WallCod Portfolio & API project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Docker & Docker Compose** - [Download](https://www.docker.com/get-started)
- **Git** - [Download](https://git-scm.com/downloads)
- **PostgreSQL 15+** (if running without Docker) - [Download](https://www.postgresql.org/download/)
- **Redis** (if running without Docker) - [Download](https://redis.io/download)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/WallCod/WallCod.git
cd WallCod
```

### 2. Environment Setup

Create environment files from examples:

```bash
# Root environment file
cp .env.example .env

# Backend environment file
cp backend/.env.example backend/.env

# Frontend environment file
cp frontend/.env.example frontend/.env
```

Edit these files with your configuration:

**.env** (root):
```env
POSTGRES_PASSWORD=your_strong_password
SECRET_KEY=your_secret_key_here
DEBUG=False
ENVIRONMENT=production
```

**backend/.env**:
```env
DATABASE_URL=postgresql://wallcod:password@localhost:5432/wallcod_db
SECRET_KEY=your_secret_key_here
DEBUG=True
ENVIRONMENT=development
```

**frontend/.env**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Option A: Running with Docker (Recommended)

#### Development Mode

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

#### Production Mode

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Option B: Running Locally

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Accessing the Application

Once running, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Initial Setup

### Creating a Test User

You can create a test user via the API:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPassword123!"
```

## Development Workflow

### Backend Development

```bash
cd backend

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run linting
black .
flake8 app/
mypy app/

# Run security checks
bandit -r app/
safety check
```

### Frontend Development

```bash
cd frontend

# Run development server
npm run dev

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build
```

## Database Management

### Running Migrations

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Database Commands

```bash
# Access PostgreSQL (in Docker)
docker exec -it wallcod_postgres_dev psql -U wallcod -d wallcod_db

# Backup database
docker exec wallcod_postgres_dev pg_dump -U wallcod wallcod_db > backup.sql

# Restore database
docker exec -i wallcod_postgres_dev psql -U wallcod wallcod_db < backup.sql
```

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

```bash
# Find process using port 8000 (backend)
lsof -i :8000
# Or on Windows:
netstat -ano | findstr :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Issues

1. Ensure PostgreSQL is running
2. Check database credentials in `.env` files
3. Verify database exists:
   ```bash
   psql -U wallcod -l
   ```

### Docker Issues

```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild containers
docker-compose build --no-cache

# View container logs
docker-compose logs -f <service-name>
```

### Permission Issues

```bash
# Fix file permissions (Linux/Mac)
sudo chown -R $USER:$USER .
```

## Next Steps

- Read the [Architecture Documentation](./architecture.md)
- Check out the [API Documentation](./api-documentation.md)
- Learn about [Security Best Practices](./security.md)
- Explore [Deployment Options](./deployment.md)

## Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/WallCod/WallCod/issues)
2. Review the documentation
3. Ask questions in the community
4. Contact the maintainer

Happy coding! 🚀
