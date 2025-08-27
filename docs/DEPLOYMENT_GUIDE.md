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
