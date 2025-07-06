# Port Configuration Summary

## Current Port Setup

### Local Development
- **Frontend**: `localhost:3000` (Next.js default)
- **Backend**: `localhost:5000` (Flask development server)

### Production Deployment
- **Frontend**: Deployed on Vercel (automatic port assignment)
- **Backend**: Deployed on Render using port `10000` (specified in render.yaml)

## Environment Variables

### Development (.env for local)
```bash
# No PORT specified for backend - defaults to 5000
# Frontend always uses 3000 in development
```

### Production (.env.example for Render)
```bash
PORT=10000  # Used by Render for backend deployment
CORS_ORIGINS=https://your-vercel-app.vercel.app  # Frontend URL
```

## Files Updated for Port Consistency

1. **backend/app.py**: Default port changed from `5001` → `5000`
2. **backend/README.md**: Examples updated to use port `5000`
3. **README.md**: Backend API URL changed from `:5001` → `:5000`
4. **Test files**: All test files updated to use port `5000`
5. **quick_test.py**: Base URL updated to use port `5000`

## Configuration Files

- **render.yaml**: Uses `$PORT` environment variable (set to 10000)
- **frontend/vercel.json**: Vercel handles port automatically
- **.env.example**: Specifies PORT=10000 for production deployment

## CORS Configuration

Backend accepts requests from:
- Local development: `http://localhost:3000` and `http://127.0.0.1:3000`
- Production: Configured via `CORS_ORIGINS` environment variable

All port configurations are now consistent across the project!
