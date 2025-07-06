@echo off
REM Deployment Preparation Script for Vercel + Render (Windows)
echo 🚀 Preparing AI-Powered Code Plagiarism Detector for deployment...

REM Check if we're in the right directory
if not exist "README.md" (
    echo ❌ Please run this script from the project root directory
    exit /b 1
)

echo 📋 Pre-deployment checklist:

REM Check backend requirements
echo 🔍 Checking backend requirements...
if exist "backend\requirements.txt" (
    echo ✅ Backend requirements.txt found
) else (
    echo ❌ Backend requirements.txt not found
    exit /b 1
)

REM Check frontend package.json
echo 🔍 Checking frontend configuration...
if exist "frontend\package.json" (
    echo ✅ Frontend package.json found
) else (
    echo ❌ Frontend package.json not found
    exit /b 1
)

REM Check if gunicorn is in requirements
findstr /C:"gunicorn" backend\requirements.txt >nul
if %errorlevel% equ 0 (
    echo ✅ Gunicorn found in requirements.txt
) else (
    echo ⚠️  Adding gunicorn to requirements.txt...
    echo gunicorn==21.2.0 >> backend\requirements.txt
)

REM Create render.yaml for easy deployment
echo 📝 Creating render.yaml for backend deployment...
(
echo services:
echo   - type: web
echo     name: plagiarism-detector-backend
echo     env: python
echo     buildCommand: pip install -r requirements.txt
echo     startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
echo     envVars:
echo       - key: FLASK_ENV
echo         value: production
echo       - key: PORT
echo         value: 10000
echo     rootDir: backend
) > render.yaml

REM Create vercel.json for frontend deployment
echo 📝 Creating vercel.json for frontend deployment...
(
echo {
echo   "framework": "nextjs",
echo   "buildCommand": "npm run build",
echo   "outputDirectory": ".next",
echo   "installCommand": "npm install"
echo }
) > frontend\vercel.json

echo ✅ Deployment preparation complete!
echo.
echo 📋 Next steps:
echo 1. Push your code to GitHub
echo 2. Deploy backend to Render:
echo    - Go to https://dashboard.render.com
echo    - Create new Web Service
echo    - Connect your GitHub repo
echo    - Set root directory to 'backend'
echo    - Add environment variables (COHERE_API_KEY, HUGGINGFACE_API_KEY)
echo.
echo 3. Deploy frontend to Vercel:
echo    - Go to https://vercel.com/dashboard
echo    - Import your GitHub repo
echo    - Set root directory to 'frontend'
echo    - Add NEXT_PUBLIC_BACKEND_URL environment variable
echo.
echo 4. Update CORS settings in backend with your Vercel URL
echo.
echo 📖 For detailed instructions, see DEPLOYMENT.md
