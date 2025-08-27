#!/bin/bash

# Oracle Fusion HCM User Management - GitHub Repository Setup Script

set -e

echo "🚀 Setting up Oracle Fusion HCM User Management GitHub Repository..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    print_warning "GitHub CLI is not installed. You'll need to create the repository manually."
    print_warning "Install GitHub CLI: https://cli.github.com/"
fi

print_header "Repository Setup"

# Get repository details
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name (default: oracle-fusion-hcm-user-management): " REPO_NAME
REPO_NAME=${REPO_NAME:-oracle-fusion-hcm-user-management}

# Update README with correct repository links
print_status "Updating README with repository information..."
sed -i.bak "s/yourusername/$GITHUB_USERNAME/g" README.md
sed -i.bak "s/oracle-fusion-hcm-user-management/$REPO_NAME/g" README.md
rm README.md.bak

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
fi

# Add all files to git
print_status "Adding files to Git..."
git add .

# Create initial commit
print_status "Creating initial commit..."
git commit -m "Initial commit: Oracle Fusion HCM User Management Tool

- FastAPI backend with Oracle Fusion HCM API integration
- Modern web frontend with responsive design
- Comprehensive user management features
- Bulk operations with Excel upload support
- Cross-platform executable support
- Docker containerization
- CI/CD pipeline with GitHub Actions"

# Create GitHub repository if GitHub CLI is available
if command -v gh &> /dev/null; then
    print_status "Creating GitHub repository..."
    gh repo create "$REPO_NAME" \
        --description "A comprehensive, modern web application for managing Oracle Fusion HCM users, roles, data security contexts, and areas of responsibility." \
        --public \
        --source=. \
        --remote=origin \
        --push
else
    print_warning "Please create the GitHub repository manually:"
    print_warning "1. Go to https://github.com/new"
    print_warning "2. Repository name: $REPO_NAME"
    print_warning "3. Description: A comprehensive, modern web application for managing Oracle Fusion HCM users, roles, data security contexts, and areas of responsibility."
    print_warning "4. Make it public"
    print_warning "5. Don't initialize with README (we already have one)"
    print_warning "6. Then run: git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    print_warning "7. Then run: git push -u origin main"
fi

print_header "Setting up GitHub Secrets"

# Check if GitHub CLI is available for secrets setup
if command -v gh &> /dev/null; then
    print_status "Setting up GitHub repository secrets..."
    
    # Ask for Docker Hub credentials
    read -p "Do you want to set up Docker Hub secrets for automated builds? (y/n): " SETUP_DOCKER
    if [[ $SETUP_DOCKER =~ ^[Yy]$ ]]; then
        read -p "Enter Docker Hub username: " DOCKER_USERNAME
        read -s -p "Enter Docker Hub password/token: " DOCKER_PASSWORD
        echo
        
        gh secret set DOCKER_USERNAME --body "$DOCKER_USERNAME"
        gh secret set DOCKER_PASSWORD --body "$DOCKER_PASSWORD"
        
        print_status "Docker Hub secrets configured."
    fi
    
    # Ask for other optional secrets
    read -p "Do you want to set up additional secrets? (y/n): " SETUP_ADDITIONAL
    if [[ $SETUP_ADDITIONAL =~ ^[Yy]$ ]]; then
        read -p "Enter any additional secret name (or press Enter to skip): " SECRET_NAME
        if [ ! -z "$SECRET_NAME" ]; then
            read -s -p "Enter secret value: " SECRET_VALUE
            echo
            gh secret set "$SECRET_NAME" --body "$SECRET_VALUE"
            print_status "Secret '$SECRET_NAME' configured."
        fi
    fi
else
    print_warning "GitHub CLI not available. Please set up secrets manually:"
    print_warning "1. Go to your repository settings"
    print_warning "2. Navigate to Secrets and variables > Actions"
    print_warning "3. Add the following secrets if needed:"
    print_warning "   - DOCKER_USERNAME: Your Docker Hub username"
    print_warning "   - DOCKER_PASSWORD: Your Docker Hub password/token"
fi

print_header "Creating Project Structure"

# Create additional directories if they don't exist
mkdir -p logs
mkdir -p uploads
mkdir -p downloads
mkdir -p docs
mkdir -p tests

# Create a basic test file
cat > tests/test_basic.py << 'EOF'
import pytest
from app.oracle_client import OracleClient

def test_oracle_client_initialization():
    """Test Oracle client initialization"""
    client = OracleClient("https://test.oraclecloud.com", "testuser", "testpass")
    assert client.base_url == "https://test.oraclecloud.com"
    assert client.username == "testuser"
    assert client.password == "testpass"

def test_api_version():
    """Test API version is set correctly"""
    client = OracleClient("https://test.oraclecloud.com", "testuser", "testpass")
    assert client.api_version == "11.13.18.05"
EOF

# Create a basic documentation file
cat > docs/API_DOCUMENTATION.md << 'EOF'
# API Documentation

## Overview
This document describes the API endpoints for the Oracle Fusion HCM User Management Tool.

## Base URL
- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication
All API calls require Oracle Fusion HCM credentials passed in the request body or query parameters.

## Endpoints

### User Management
- `GET /users/` - Get all users
- `POST /users/details` - Get comprehensive user details
- `POST /users/roles/assign` - Assign role to user
- `POST /users/roles/remove` - Remove role from user
- `POST /users/roles/bulk-assign` - Bulk role assignment

### Data Security
- `POST /users/data-security/assign` - Assign data security context
- `POST /users/data-security/bulk-assign` - Bulk data security assignment

### Areas of Responsibility
- `GET /areas-of-responsibility/` - Get all AORs
- `POST /areas-of-responsibility/assign` - Assign AOR to user
- `POST /areas-of-responsibility/remove` - Remove AOR from user
- `POST /areas-of-responsibility/bulk-assign` - Bulk AOR assignment

### Password Management
- `POST /users/password/reset` - Reset user password
- `POST /users/password/update` - Update user password

### File Operations
- `POST /upload/excel` - Upload Excel file for bulk operations
- `GET /users/download` - Download users as Excel file

### Search
- `POST /users/search` - Search users with criteria
- `POST /areas-of-responsibility/search` - Search AORs

## Error Handling
All endpoints return appropriate HTTP status codes and error messages in JSON format.

## Rate Limiting
API calls are subject to rate limiting based on Oracle Fusion HCM API limits.
EOF

# Create a deployment guide
cat > docs/DEPLOYMENT_GUIDE.md << 'EOF'
# Deployment Guide

## Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `uvicorn app.main:app --reload`
4. Open `frontend/index.html` in your browser

## Docker Deployment
1. Build the image: `docker build -t oracle-fusion-hcm .`
2. Run the container: `docker run -p 8000:8000 oracle-fusion-hcm`

## Docker Compose Deployment
1. Run: `docker-compose up -d`
2. Access the application at `http://localhost:8000`

## Production Deployment
1. Use Docker Compose with production profile
2. Configure reverse proxy (nginx)
3. Set up SSL certificates
4. Configure monitoring and logging

## Cloud Deployment
### AWS
- Use ECS or EKS for container deployment
- Use ALB for load balancing
- Use CloudWatch for monitoring

### Azure
- Use Azure Container Instances or AKS
- Use Application Gateway for load balancing
- Use Azure Monitor for monitoring

### Google Cloud
- Use Cloud Run or GKE
- Use Cloud Load Balancing
- Use Cloud Monitoring
EOF

print_header "Setting up Development Environment"

# Create a development requirements file
cat > requirements-dev.txt << 'EOF'
# Development dependencies
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.0.0
bandit==1.7.5
mypy==1.5.1
pre-commit==3.3.3
EOF

# Create a pre-commit configuration
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
EOF

print_header "Final Steps"

print_status "Repository setup complete!"
echo
print_status "Next steps:"
echo "1. Review the generated files and customize as needed"
echo "2. Test the application locally"
echo "3. Push changes to GitHub: git push origin main"
echo "4. Set up GitHub Pages for documentation (optional)"
echo "5. Configure branch protection rules"
echo "6. Set up issue templates and pull request templates"
echo
print_status "Useful commands:"
echo "- Start development server: uvicorn app.main:app --reload"
echo "- Run tests: pytest"
echo "- Format code: black app/"
echo "- Lint code: flake8 app/"
echo "- Build Docker image: docker build -t oracle-fusion-hcm ."
echo "- Run with Docker Compose: docker-compose up -d"
echo
print_status "Documentation created:"
echo "- docs/API_DOCUMENTATION.md"
echo "- docs/DEPLOYMENT_GUIDE.md"
echo "- README.md (updated with repository links)"
echo
print_status "Happy coding! 🎉"
