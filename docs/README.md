# WallCod Portfolio & API Documentation

Complete documentation for the WallCod Portfolio and API project.

## Table of Contents

1. [Getting Started](./getting-started.md)
2. [Architecture](./architecture.md)
3. [API Documentation](./api-documentation.md)
4. [Security](./security.md)
5. [Deployment](./deployment.md)
6. [Contributing](./contributing.md)

## Quick Links

- **Live Site**: [Coming Soon]
- **API Documentation**: http://localhost:8000/docs (when running locally)
- **GitHub Repository**: https://github.com/WallCod/WallCod

## Overview

This is a full-stack portfolio and API project built with modern technologies:

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 14 (TypeScript)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Features

- 🔐 **Authentication & Authorization** - JWT-based auth with refresh tokens
- 🛡️ **Security First** - Input validation, rate limiting, CORS, security headers
- 📊 **API Documentation** - Auto-generated OpenAPI/Swagger docs
- 🧪 **Testing** - Unit, integration, and security tests
- 🐳 **Docker Support** - Full containerization with Docker Compose
- ⚡ **Performance** - Redis caching, database optimization
- 🔄 **CI/CD** - Automated testing and deployment
- 📱 **Responsive Design** - Mobile-first approach
- 🌙 **Dark Mode** - Theme support
- 📈 **Monitoring** - Health checks and logging

## Technologies

### Backend

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Alembic** - Database migrations
- **Redis** - Caching and session storage
- **JWT** - Authentication tokens
- **Pytest** - Testing framework

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **SWR** - Data fetching and caching
- **Zustand** - State management
- **React Hook Form** - Form handling
- **Zod** - Schema validation

### DevOps

- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipelines
- **PostgreSQL** - Relational database
- **Nginx** - Reverse proxy (optional)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/WallCod/WallCod.git
cd WallCod

# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start with Docker Compose (Development)
docker-compose -f docker-compose.dev.yml up -d

# Or start services individually
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
WallCod/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality (config, security, db)
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── tests/          # Tests
│   ├── alembic/            # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities
│   │   └── types/         # TypeScript types
│   ├── Dockerfile
│   └── package.json
├── .github/
│   └── workflows/         # CI/CD pipelines
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── docker-compose.yml     # Production compose file
└── docker-compose.dev.yml # Development compose file
```

## License

MIT License - see LICENSE file for details

## Contact

- **GitHub**: [@WallCod](https://github.com/WallCod)
- **LinkedIn**: [Wallax Figueiredo](https://www.linkedin.com/in/wallax-figueiredo-41116b285/)
- **Twitter**: [@black14691](https://x.com/black14691)
- **Website**: www.alphalabs.lat
