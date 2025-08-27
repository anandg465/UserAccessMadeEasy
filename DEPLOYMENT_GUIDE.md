# 🚀 Oracle Fusion HCM User Management Tool - Deployment Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Development Environment](#development-environment)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Oracle Fusion HCM instance with API access
- Modern web browser

### 1. Clone the Repository
```bash
git clone https://github.com/anandg465/UserAccessMadeEasy.git
cd UserAccessMadeEasy
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the Application
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: Open `frontend/index.html` in your browser

## 🛠️ Development Environment

### Running Tests
```bash
# Run all tests
PYTHONPATH=. pytest tests/ -v

# Run tests with coverage
PYTHONPATH=. pytest tests/ -v --cov=app --cov-report=html

# Run linting
flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127

# Run security scan
bandit -r app/ -f json -o bandit-report.json

# Format code
black app/
```

### Development Workflow
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test locally

3. **Run quality checks**:
   ```bash
   # Format code
   black app/
   
   # Run tests
   PYTHONPATH=. pytest tests/ -v
   
   # Run linting
   flake8 app/
   ```

4. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

## 🏭 Production Deployment

### Option 1: Direct Server Deployment

#### 1. Server Requirements
- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- Nginx (for reverse proxy)
- Systemd (for service management)

#### 2. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/anandg465/UserAccessMadeEasy.git
cd UserAccessMadeEasy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Create Systemd Service
Create `/etc/systemd/system/oracle-fusion-hcm.service`:
```ini
[Unit]
Description=Oracle Fusion HCM User Management Tool
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/UserAccessMadeEasy
Environment=PATH=/path/to/UserAccessMadeEasy/venv/bin
ExecStart=/path/to/UserAccessMadeEasy/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Configure Nginx
Create `/etc/nginx/sites-available/oracle-fusion-hcm`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    location / {
        root /path/to/UserAccessMadeEasy/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API documentation
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5. Enable and Start Services
```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/oracle-fusion-hcm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable and start application service
sudo systemctl enable oracle-fusion-hcm
sudo systemctl start oracle-fusion-hcm
sudo systemctl status oracle-fusion-hcm
```

### Option 2: Docker Deployment

#### 1. Build Docker Image
```bash
docker build -t oracle-fusion-hcm .
```

#### 2. Run with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 3. Production Docker Compose
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  oracle-fusion-hcm:
    build: .
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
      - ./downloads:/app/downloads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend:/usr/share/nginx/html
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - oracle-fusion-hcm
```

## ☁️ Cloud Deployment

### AWS Deployment

#### 1. EC2 Instance Setup
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Connect via SSH and follow the Direct Server Deployment steps above
```

#### 2. AWS Load Balancer
- Create Application Load Balancer
- Configure target group pointing to EC2 instance
- Set up SSL certificate in AWS Certificate Manager

#### 3. Auto Scaling Group
- Create launch template with user data script
- Configure auto scaling group for high availability

### Azure Deployment

#### 1. Azure App Service
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name oracle-fusion-rg --location eastus

# Create app service plan
az appservice plan create --name oracle-fusion-plan --resource-group oracle-fusion-rg --sku B1

# Create web app
az webapp create --name oracle-fusion-app --resource-group oracle-fusion-rg --plan oracle-fusion-plan --runtime "PYTHON|3.9"
```

#### 2. Deploy Application
```bash
# Deploy from local directory
az webapp deployment source config-local-git --name oracle-fusion-app --resource-group oracle-fusion-rg

# Push to Azure
git remote add azure <azure-git-url>
git push azure main
```

### Google Cloud Platform

#### 1. App Engine Deployment
Create `app.yaml`:
```yaml
runtime: python39
entrypoint: uvicorn app.main:app --host 0.0.0.0 --port $PORT

env_variables:
  ENVIRONMENT: production

handlers:
  - url: /static
    static_dir: frontend
  - url: /.*
    script: auto
```

#### 2. Deploy to App Engine
```bash
# Install Google Cloud SDK
# Deploy application
gcloud app deploy
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### 2. Permission Issues
```bash
# Fix file permissions
sudo chown -R www-data:www-data /path/to/UserAccessMadeEasy
sudo chmod -R 755 /path/to/UserAccessMadeEasy
```

#### 3. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Database Connection Issues
- Check Oracle Fusion API credentials
- Verify network connectivity
- Check firewall settings

### Logs and Monitoring

#### 1. Application Logs
```bash
# View application logs
sudo journalctl -u oracle-fusion-hcm -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### 2. Docker Logs
```bash
# View container logs
docker-compose logs -f oracle-fusion-hcm

# View specific service logs
docker logs <container-id>
```

## 🔒 Security Considerations

### 1. Environment Variables
```bash
# Create .env file for sensitive data
cat > .env << EOF
ORACLE_INSTANCE_URL=your-oracle-instance-url
ORACLE_USERNAME=your-username
ORACLE_PASSWORD=your-password
SECRET_KEY=your-secret-key
EOF
```

### 2. SSL/TLS Configuration
```bash
# Install SSL certificate
sudo certbot --nginx -d your-domain.com

# Configure HTTPS redirect in Nginx
```

### 3. Firewall Configuration
```bash
# Configure UFW firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 4. Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip install --upgrade -r requirements.txt
```

## 📊 Monitoring and Maintenance

### 1. Health Checks
```bash
# Create health check script
cat > health_check.sh << 'EOF'
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ $response -eq 200 ]; then
    echo "Application is healthy"
    exit 0
else
    echo "Application is unhealthy"
    exit 1
fi
EOF

chmod +x health_check.sh
```

### 2. Backup Strategy
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /path/to/UserAccessMadeEasy

# Backup logs
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz /var/log/oracle-fusion-hcm

echo "Backup completed: $DATE"
EOF

chmod +x backup.sh
```

### 3. Performance Monitoring
- Set up Prometheus and Grafana for metrics
- Monitor CPU, memory, and disk usage
- Set up alerts for critical thresholds

## 📞 Support

### Getting Help
1. **Documentation**: Check the [README.md](README.md) for detailed information
2. **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/anandg465/UserAccessMadeEasy/issues)
3. **Discussions**: Join [GitHub Discussions](https://github.com/anandg465/UserAccessMadeEasy/discussions) for community support

### Contact Information
- **Repository**: https://github.com/anandg465/UserAccessMadeEasy
- **Maintainer**: anandg465
- **Email**: anand.gaurav@hotmail.com

---

**Note**: This deployment guide assumes you have proper Oracle Fusion HCM API access and permissions. Ensure compliance with your organization's security policies and Oracle's terms of service.
