from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import comparison, health

app = FastAPI(title="Code Plagiarism Detector API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(comparison.router, prefix="/api/comparison", tags=["comparison"])
app.include_router(health.router, prefix="/api", tags=["health"])

@app.get("/")
async def root():
    """Root endpoint - redirect to docs."""
    return {"message": "Welcome to the Code Plagiarism Detector API. Visit /docs for documentation."}
