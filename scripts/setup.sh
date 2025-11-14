#!/bin/bash

# WallCod Portfolio Setup Script
# This script automates the initial setup process

set -e  # Exit on error

echo "🚀 WallCod Portfolio Setup"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if required commands exist
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 is not installed${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 is installed${NC}"
        return 0
    fi
}

echo "Checking prerequisites..."
echo ""

# Check prerequisites
MISSING_DEPS=0

if ! check_command "python3"; then MISSING_DEPS=1; fi
if ! check_command "node"; then MISSING_DEPS=1; fi
if ! check_command "docker"; then MISSING_DEPS=1; fi
if ! check_command "docker-compose"; then MISSING_DEPS=1; fi

echo ""

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${RED}Please install missing dependencies before continuing${NC}"
    exit 1
fi

# Create environment files
echo "Creating environment files..."

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env${NC}"
else
    echo -e "${YELLOW}⚠ .env already exists${NC}"
fi

if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${YELLOW}⚠ backend/.env already exists${NC}"
fi

if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓ Created frontend/.env${NC}"
else
    echo -e "${YELLOW}⚠ frontend/.env already exists${NC}"
fi

echo ""

# Generate secret key
echo "Generating secret key..."
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/g" backend/.env
echo -e "${GREEN}✓ Secret key generated${NC}"

echo ""

# Ask for setup method
echo "Choose setup method:"
echo "1) Docker (recommended)"
echo "2) Local development"
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo ""
        echo "Starting Docker setup..."
        echo ""

        # Build and start containers
        docker-compose -f docker-compose.dev.yml up -d --build

        echo ""
        echo -e "${GREEN}✓ Docker containers started${NC}"
        echo ""
        echo "Services are running at:"
        echo "  Frontend: http://localhost:3000"
        echo "  Backend:  http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo ""
        echo "View logs with:"
        echo "  docker-compose -f docker-compose.dev.yml logs -f"
        ;;

    2)
        echo ""
        echo "Setting up local development..."
        echo ""

        # Backend setup
        echo "Setting up backend..."
        cd backend

        if [ ! -d "venv" ]; then
            python3 -m venv venv
            echo -e "${GREEN}✓ Created virtual environment${NC}"
        fi

        source venv/bin/activate
        pip install -r requirements.txt
        echo -e "${GREEN}✓ Installed backend dependencies${NC}"

        cd ..

        # Frontend setup
        echo "Setting up frontend..."
        cd frontend
        npm install
        echo -e "${GREEN}✓ Installed frontend dependencies${NC}"

        cd ..

        echo ""
        echo -e "${GREEN}✓ Local setup complete${NC}"
        echo ""
        echo "To start the backend:"
        echo "  cd backend"
        echo "  source venv/bin/activate"
        echo "  uvicorn app.main:app --reload"
        echo ""
        echo "To start the frontend:"
        echo "  cd frontend"
        echo "  npm run dev"
        ;;

    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Setup complete! 🎉${NC}"
echo ""
echo "Next steps:"
echo "  1. Review and update environment variables in .env files"
echo "  2. Read the documentation in docs/"
echo "  3. Start developing!"
echo ""
