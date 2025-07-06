# 🌐 Web-Based Deployment Guide
## Deploy without CLI - Using Only Web Interfaces

### Prerequisites ✅
- [ ] GitHub account with your code repository
- [ ] Git LFS set up (see DEPLOYMENT.md for details)
- [ ] API Keys: Cohere and Hugging Face
- [ ] Render account (free tier available)
- [ ] Vercel account (free tier available)

---

## 🔄 Step 1: Prepare Your Repository

### Push to GitHub:
1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Verify Git LFS files**:
   - Go to your GitHub repository
   - Check that large files show "Stored with Git LFS" label
   - If not, make sure `.gitattributes` is committed

---

## 🎯 Step 2: Deploy Backend to Render

### 2.1 Create Render Account
1. Go to **[https://render.com](https://render.com)**
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### 2.2 Create Web Service
1. From Render Dashboard, click **"New +"** → **"Web Service"**
2. **Connect Repository**:
   - Select "Build and deploy from a Git repository"
   - Click "Connect" next to your GitHub account
   - Find and select your repository
   - Click "Connect"

### 2.3 Configure Service Settings
**Basic Settings:**
- **Name**: `plagiarism-detector-backend`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend`

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

**Instance Type:**
- **Free Tier**: `Free` (512MB RAM, sleeps after 15min inactivity)
- **Paid**: `Starter` ($7/month, always on) - recommended for production

### 2.4 Environment Variables
In the "Environment" section, add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `COHERE_API_KEY` | `your_cohere_api_key` | Required |
| `HUGGINGFACE_API_KEY` | `your_huggingface_api_key` | Required |
| `FLASK_ENV` | `production` | Required |
| `PORT` | `10000` | Required |
| `SECRET_KEY` | `your_secure_random_key` | Generate a strong key |
| `CORS_ORIGINS` | `https://your-app.vercel.app` | Update after frontend deploy |

### 2.5 Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. **Save your backend URL**: `https://your-service.onrender.com`

---

## ⚡ Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account
1. Go to **[https://vercel.com](https://vercel.com)**
2. Click "Start Deploying"
3. Sign up with GitHub (recommended)

### 3.2 Import Project
1. From Vercel Dashboard, click **"New Project"**
2. **Import Git Repository**:
   - Find your repository in the list
   - Click "Import"

### 3.3 Configure Project Settings
**Framework Preset**: Vercel should auto-detect "Next.js"

**Build and Output Settings**:
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (usually auto-detected)
- **Output Directory**: `.next` (usually auto-detected)
- **Install Command**: `npm install` (usually auto-detected)

### 3.4 Environment Variables
Add these in the "Environment Variables" section:

| Key | Value | Environment |
|-----|-------|-------------|
| `NEXT_PUBLIC_BACKEND_URL` | `https://your-render-service.onrender.com` | Production |
| `NODE_ENV` | `production` | Production |

### 3.5 Deploy
1. Click **"Deploy"**
2. Wait for deployment (2-5 minutes)
3. **Save your frontend URL**: `https://your-app.vercel.app`

---

## 🔗 Step 4: Update CORS Settings

### Update Backend CORS:
1. Go back to **Render Dashboard**
2. Select your backend service
3. Go to **"Environment"** tab
4. Update `CORS_ORIGINS` with your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
5. Click **"Save Changes"**
6. Service will automatically redeploy

---

## 🧪 Step 5: Test Your Deployment

### Quick Tests:
1. **Backend Health Check**:
   - Visit: `https://your-render-service.onrender.com/health`
   - Should return: `{"status": "healthy"}`

2. **Frontend Loading**:
   - Visit: `https://your-app.vercel.app`
   - Should load the web interface

3. **API Integration**:
   - Try analyzing code through the web interface
   - Check browser console for any errors

---

## 🎨 Step 6: Custom Domains (Optional)

### Vercel Custom Domain:
1. In Vercel project settings → **"Domains"**
2. Add your custom domain
3. Follow DNS configuration instructions

### Render Custom Domain:
1. In Render service settings → **"Custom Domains"**
2. Add your custom domain
3. Follow DNS configuration instructions

---

## 🚨 Troubleshooting

### Common Issues:

**Backend Issues:**
- **Build fails**: Check `requirements.txt` has all dependencies
- **App won't start**: Verify `app:app` in start command
- **API errors**: Check environment variables are set correctly

**Frontend Issues:**
- **Build fails**: Check `package.json` scripts
- **API calls fail**: Verify `NEXT_PUBLIC_BACKEND_URL` is correct
- **CORS errors**: Update backend `CORS_ORIGINS`

**Git LFS Issues:**
- **Large files not uploading**: Check `.gitattributes` configuration
- **Deployment fails with large files**: Ensure LFS is enabled on repository

### Monitoring:
- **Render**: Check logs in service dashboard
- **Vercel**: Check function logs in project dashboard
- **Performance**: Both platforms provide analytics

---

## 📊 Cost Breakdown

### Free Tier Limits:
**Render Free:**
- 512MB RAM
- Sleeps after 15min inactivity
- 750 hours/month

**Vercel Free:**
- 100GB bandwidth/month
- 6,000 build minutes/month
- Unlimited static sites

### Recommended Upgrades:
- **Render Starter** ($7/month): Always-on backend
- **Vercel Pro** ($20/month): Better performance, analytics

---

## ✅ Success Checklist

- [ ] Backend deployed and health check passes
- [ ] Frontend deployed and loads correctly
- [ ] API integration working (test code analysis)
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Custom domains configured (if needed)
- [ ] Monitoring set up

**🎉 Your AI-Powered Code Plagiarism Detector is now live!**
