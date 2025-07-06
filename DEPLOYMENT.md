# Deployment Guide

This guide covers deployment of the AI-Powered Code Plagiarism Detector using Vercel (frontend) and Render (backend).

## 🗂️ Git LFS Setup (Required)

**Important**: This project uses large AI model files that require Git LFS (Large File Storage).

### Setup Git LFS:
1. **Install Git LFS** (if not already installed):
   ```bash
   # Download from: https://git-lfs.github.io/
   git lfs install
   ```

2. **Track large files** (already configured in `.gitattributes`):
   - Model files: `*.bin`, `*.h5`, `*.pt`, `*.pth`, `*.onnx`
   - Native modules: `*.dll`, `*.so`, `*.dylib`, `*.node`
   - Large data files: `*.zip`, `*.tar.gz`

3. **Verify LFS setup**:
   ```bash
   git lfs track
   ```

### Important Notes:
- **GitHub**: Free tier includes 1GB LFS storage, 1GB/month bandwidth
- **Render**: Automatically handles Git LFS during deployment
- **Vercel**: Supports Git LFS for build files

## 🚀 Quick Start

### Prerequisites
- GitHub/GitLab repository with your code
- API keys for Cohere and Hugging Face
- Vercel account (free tier available)
- Render account (free tier available)

### Architecture
- **Frontend**: Next.js app deployed to Vercel
- **Backend**: Flask API deployed to Render
- **Database**: In-memory storage (can be upgraded to persistent database on Render)

## 🎯 Step-by-Step Deployment

### Step 1: Deploy Backend to Render

1. **Create a new Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:

2. **Service Configuration**:
   ```
   Name: plagiarism-detector-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

3. **Environment Variables** (Add in Render dashboard):
   ```
   COHERE_API_KEY=your_cohere_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   FLASK_ENV=production
   PORT=10000
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

4. **Build Settings**:
   - Root Directory: `backend`
   - Python Version: 3.11 (or your preferred version)

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy via Vercel Dashboard**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Configure the project:

3. **Project Configuration**:
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

4. **Environment Variables** (Add in Vercel dashboard):
   ```
   NEXT_PUBLIC_BACKEND_URL=https://your-render-service.onrender.com
   NODE_ENV=production
   ```

### Step 3: Configure CORS

Update your backend CORS settings with your Vercel domain:
```python
# In backend/config.py
CORS_ORIGINS = [
    "https://your-vercel-app.vercel.app",
    "https://your-custom-domain.com",  # if you have a custom domain
]
```

## 🔧 Configuration Files

### Backend Requirements (requirements.txt)
Ensure your `backend/requirements.txt` includes:
```
flask==2.3.2
flask-cors==4.0.0
gunicorn==21.2.0
requests==2.31.0
cohere==4.21.0
# ... other dependencies
```

### Frontend Package.json Scripts
Ensure your `frontend/package.json` has:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

## 🌐 Custom Domains (Optional)

### Vercel Custom Domain
1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Render Custom Domain
1. Go to your service settings in Render
2. Navigate to "Custom Domains"
3. Add your custom domain
4. Update DNS records as instructed

## 📊 Environment Variables Reference

### Backend Environment Variables
```bash
# Required
COHERE_API_KEY=your_cohere_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Production Settings
FLASK_ENV=production
PORT=10000

# CORS (Update with your actual Vercel URL)
CORS_ORIGINS=https://your-vercel-app.vercel.app

# Optional
SECRET_KEY=your_secure_secret_key
LOG_LEVEL=INFO
```

### Frontend Environment Variables
```bash
# Required
NEXT_PUBLIC_BACKEND_URL=https://your-render-service.onrender.com

# Production Settings
NODE_ENV=production
```

## 📊 Monitoring and Health Checks

### Health Endpoints
- **Backend**: `GET https://your-render-service.onrender.com/health`
- **Frontend**: `GET https://your-vercel-app.vercel.app/`

### Render Monitoring
- Automatic health checks
- Built-in metrics dashboard
- Log streaming in dashboard
- Automatic deployments on git push

### Vercel Monitoring
- Built-in analytics
- Performance insights
- Function logs
- Automatic deployments on git push

## 🚀 Deployment Automation

### Automatic Deployments
Both Vercel and Render support automatic deployments:

1. **Render**: Automatically deploys when you push to your main branch
2. **Vercel**: Automatically deploys on every push, with preview deployments for branches

### Environment-specific Deployments
- **Production**: Deploy from `main` branch
- **Staging**: Deploy from `develop` branch (configure separate services)

## � Security Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use platform-specific environment variable management
3. **CORS**: Configure restrictive CORS policies
4. **HTTPS**: Both platforms provide HTTPS by default
5. **Rate Limiting**: Implement in backend code (not infrastructure level)

## � Cost Considerations

### Free Tier Limits

**Render Free Tier**:
- 750 hours/month
- Goes to sleep after 15 minutes of inactivity
- Slower cold starts
- 512MB RAM

**Vercel Free Tier**:
- 100GB bandwidth/month
- 6,000 minutes build time/month
- Unlimited static deployments

### Upgrading
- **Render**: $7/month for always-on service
- **Vercel**: $20/month per member for Pro features

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check build logs in Render/Vercel dashboards
   - Verify all dependencies are in requirements.txt/package.json
   - Ensure Python/Node versions are compatible

2. **CORS Errors**:
   - Verify CORS_ORIGINS in backend environment variables
   - Check that frontend URL matches exactly (including https://)
   - Ensure no trailing slashes in URLs

3. **API Connection Issues**:
   - Verify NEXT_PUBLIC_BACKEND_URL is set correctly
   - Check that backend service is running and accessible
   - Test backend health endpoint directly

4. **Environment Variable Issues**:
   - Double-check all environment variables are set
   - Verify no extra spaces in variable names/values
   - Check that secrets are properly configured

5. **Cold Start Delays** (Render Free Tier):
   - First request after 15 minutes may be slow
   - Consider upgrading to paid plan for always-on service

### Performance Optimization

1. **Backend Optimization**:
   - Use gunicorn with multiple workers
   - Implement caching for AI model responses
   - Optimize database queries

2. **Frontend Optimization**:
   - Next.js automatic optimization
   - Image optimization with Next.js Image component
   - Static generation where possible

## 📞 Getting Help

### Platform-specific Support
- **Render**: [Render Docs](https://render.com/docs) and [Community Forum](https://community.render.com)
- **Vercel**: [Vercel Docs](https://vercel.com/docs) and [GitHub Discussions](https://github.com/vercel/vercel/discussions)

### Debugging Steps
1. Check service status on platform dashboards
2. Review deployment logs
3. Test API endpoints individually
4. Verify environment variables
5. Check network connectivity between services

## ✅ Pre-deployment Checklist

- [ ] All environment variables configured
- [ ] CORS settings updated with production URLs
- [ ] API keys obtained and tested
- [ ] Frontend backend URL updated
- [ ] Requirements.txt/package.json up to date
- [ ] Health endpoints working
- [ ] Test deployment in staging environment
- [ ] Monitor logs after deployment
