#!/bin/bash

# Test runner script for WallCod Portfolio

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧪 Running Tests${NC}"
echo "==============="
echo ""

# Parse arguments
RUN_BACKEND=true
RUN_FRONTEND=true
RUN_SECURITY=false
COVERAGE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            RUN_FRONTEND=false
            shift
            ;;
        --frontend-only)
            RUN_BACKEND=false
            shift
            ;;
        --security)
            RUN_SECURITY=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Backend tests
if [ "$RUN_BACKEND" = true ]; then
    echo -e "${BLUE}Running backend tests...${NC}"
    cd backend

    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    if [ "$COVERAGE" = true ]; then
        pytest --cov=app --cov-report=html --cov-report=term-missing
    else
        pytest
    fi

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Backend tests passed${NC}"
    else
        echo -e "${RED}✗ Backend tests failed${NC}"
        exit 1
    fi

    cd ..
    echo ""
fi

# Frontend tests
if [ "$RUN_FRONTEND" = true ]; then
    echo -e "${BLUE}Running frontend tests...${NC}"
    cd frontend

    if [ "$COVERAGE" = true ]; then
        npm run test:coverage
    else
        npm test
    fi

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Frontend tests passed${NC}"
    else
        echo -e "${RED}✗ Frontend tests failed${NC}"
        exit 1
    fi

    cd ..
    echo ""
fi

# Security tests
if [ "$RUN_SECURITY" = true ]; then
    echo -e "${BLUE}Running security checks...${NC}"

    # Backend security
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    echo "Running Bandit..."
    bandit -r app/ -ll

    echo "Running Safety check..."
    safety check

    cd ..

    echo -e "${GREEN}✓ Security checks passed${NC}"
    echo ""
fi

echo ""
echo -e "${GREEN}All tests completed successfully! ✅${NC}"
