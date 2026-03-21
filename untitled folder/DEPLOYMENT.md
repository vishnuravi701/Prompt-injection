# Deployment Guide

## Local Development

See [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) for local setup.

## Docker Deployment

### Build Images

```bash
# Build both images
docker-compose build

# Start services
docker-compose up
```

Access:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Individual Container Builds

**Backend:**
```bash
cd backend
docker build -t prompt-injection-api:latest .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key prompt-injection-api:latest
```

**Frontend:**
```bash
cd frontend
docker build -t prompt-injection-ui:latest .
docker run -p 3000:3000 prompt-injection-ui:latest
```

## Azure Deployment

### Prerequisites
- Azure subscription
- Azure CLI installed
- Docker images built

### Option 1: Azure Container Instances (Easiest)

```bash
# Create resource group
az group create --name MyResourceGroup --location eastus

# Deploy backend
az container create \
  --resource-group MyResourceGroup \
  --name prompt-injection-api \
  --image prompt-injection-api:latest \
  --ports 8000 \
  --memory 2 \
  --environment-variables GEMINI_API_KEY=your_key

# Deploy frontend
az container create \
  --resource-group MyResourceGroup \
  --name prompt-injection-ui \
  --image prompt-injection-ui:latest \
  --ports 3000 \
  --memory 1
```

### Option 2: App Service

```bash
# Create service plan
az appservice plan create \
  --name MyAppPlan \
  --resource-group MyResourceGroup \
  --sku B1 \
  --is-linux

# Create web app for backend
az webapp create \
  --resource-group MyResourceGroup \
  --plan MyAppPlan \
  --name prompt-injection-api \
  --deployment-container-image-name prompt-injection-api:latest

# Configure deployment
az webapp config container set \
  --resource-group MyResourceGroup \
  --name prompt-injection-api \
  --docker-custom-image-name prompt-injection-api:latest \
  --docker-registry-server-url https://registry.hub.docker.com
```

### Option 3: Azure Kubernetes Service (AKS)

```bash
# Create AKS cluster
az aks create \
  --resource-group MyResourceGroup \
  --name MyAKSCluster \
  --node-count 2 \
  --enable-managed-identity

# Get credentials
az aks get-credentials \
  --resource-group MyResourceGroup \
  --name MyAKSCluster

# Deploy with kubectl (requires k8s manifests)
kubectl apply -f k8s-manifests/
```

## Environment Variables for Production

Create `.env.production`:

```
# API Configuration  
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Gemini API
GEMINI_API_KEY=your_production_key

# Model Paths (use Azure Blob Storage paths)
MODEL_PATH=/mnt/models/model.pkl
PREPROCESSOR_PATH=/mnt/models/preprocessor.pkl

# Frontend
REACT_APP_API_URL=https://your-api-domain.com

# CORS
CORS_ORIGINS=https://your-frontend-domain.com

# Logging
LOG_LEVEL=WARNING

# Security
SECURE_COOKIES=true
HTTPS_ONLY=true
```

## SSL/HTTPS

### Using Let's Encrypt

```bash
# For App Service
az webapp config ssl create \
  --resource-group MyResourceGroup \
  --name prompt-injection-api \
  --certificate-file certificate.pfx \
  --certificate-password password
```

### For Custom Domain

```bash
az app service domain create \
  --name your-domain.com \
  --resource-group MyResourceGroup
```

## Database Integration (Optional)

For production with user history:

```bash
# Create Azure SQL Database
az sql server create \
  --resource-group MyResourceGroup \
  --name sql-server-name \
  --admin-user admin \
  --admin-password password

az sql db create \
  --resource-group MyResourceGroup \
  --server sql-server-name \
  --name prompt-injection-db
```

## Monitoring & Logging

### Azure Application Insights

```bash
# Create Application Insights resource
az monitor app-insights component create \
  --resource-group MyResourceGroup \
  --app my-app-insights \
  --location eastus
```

Add to backend code:
```python
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor()
```

### Logs

```bash
# View logs
az container logs \
  --resource-group MyResourceGroup \
  --name prompt-injection-api

# Stream logs
az container attach \
  --resource-group MyResourceGroup \
  --name prompt-injection-api
```

## Auto-Scaling

### For App Service

```bash
# Create auto scale settings
az monitor metrics alert create \
  --resource-group MyResourceGroup \
  --name high-cpu \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Web/serverfarms/{app-plan}
```

### For AKS

```bash
# Enable horizontal pod autoscaler
kubectl autoscale deployment prompt-injection-api --min=2 --max=10
```

## Health Checks

Backend implements `/health` endpoint:

```bash
curl https://your-api-domain.com/health
# Returns: {"status": "healthy", "version": "1.0.0"}
```

Configure health checks in Azure:
```bash
az webapp config set \
  --resource-group MyResourceGroup \
  --name prompt-injection-api \
  --generic-configurations '{"healthCheckPath": "/health"}'
```

## Backup & Recovery

### Database Backup

```bash
# Enable automated backups
az sql db update \
  --resource-group MyResourceGroup \
  --server sql-server-name \
  --name prompt-injection-db \
  --backup-storage-redundancy Geo
```

### Model Backup

Store models in Azure Blob Storage:
```bash
az storage blob upload \
  --account-name mystorageaccount \
  --container-name models \
  --name model.pkl \
  --file ./models/trained_model/model.pkl
```

## Troubleshooting Deployment

**Container won't start:**
- Check logs: `az container logs --name container-name --resource-group rg`
- Verify environment variables
- Check image exists in registry

**Connection errors:**
- Check security groups/firewalls
- Verify CORS configuration
- Check API key permissions

**Performance issues:**
- Increase container memory limits
- Enable caching
- Consider CDN for static files

## Cost Optimization

- Use B1 tier for App Service
- Set auto-shutdown for dev environments
- Use spot instances for AKS
- Enable data redundancy selectively
- Monitor and optimize resource usage

## Production Checklist

- [ ] SSL certificate installed
- [ ] Environment variables configured
- [ ] Database configured
- [ ] Backup strategy in place
- [ ] Monitoring enabled
- [ ] Auto-scaling configured
- [ ] Logging configured
- [ ] Security groups configured
- [ ] DNS records updated
- [ ] Load testing completed
- [ ] Disaster recovery plan
- [ ] Documentation updated

For more Azure-specific guidance, see Azure documentation or contact Azure support.
