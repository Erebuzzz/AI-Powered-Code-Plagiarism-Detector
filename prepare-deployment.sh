#!/bin/bash

# Deployment Preparation Script for Vercel + Render
echo "🚀 Preparing AI-Powered Code Plagiarism Detector for deployment..."

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📋 Pre-deployment checklist:"

# Check backend requirements
echo "🔍 Checking backend requirements..."
if [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend requirements.txt found"
else
    echo "❌ Backend requirements.txt not found"
    exit 1
fi

# Check frontend package.json
echo "🔍 Checking frontend configuration..."
if [ -f "frontend/package.json" ]; then
    echo "✅ Frontend package.json found"
else
    echo "❌ Frontend package.json not found"
    exit 1
fi

# Check if gunicorn is in requirements
if grep -q "gunicorn" backend/requirements.txt; then
    echo "✅ Gunicorn found in requirements.txt"
else
    echo "⚠️  Adding gunicorn to requirements.txt..."
    echo "gunicorn==21.2.0" >> backend/requirements.txt
fi

# Create render.yaml for easy deployment
echo "📝 Creating render.yaml for backend deployment..."
cat > render.yaml << EOF
services:
  - type: web
    name: plagiarism-detector-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 10000
    rootDir: backend
EOF

# Create vercel.json for frontend deployment
echo "📝 Creating vercel.json for frontend deployment..."
cat > frontend/vercel.json << EOF
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install"
}
EOF

echo "✅ Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Deploy backend to Render:"
echo "   - Go to https://dashboard.render.com"
echo "   - Create new Web Service"
echo "   - Connect your GitHub repo"
echo "   - Set root directory to 'backend'"
echo "   - Add environment variables (COHERE_API_KEY, HUGGINGFACE_API_KEY)"
echo ""
echo "3. Deploy frontend to Vercel:"
echo "   - Go to https://vercel.com/dashboard"
echo "   - Import your GitHub repo"
echo "   - Set root directory to 'frontend'"
echo "   - Add NEXT_PUBLIC_BACKEND_URL environment variable"
echo ""
echo "4. Update CORS settings in backend with your Vercel URL"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
