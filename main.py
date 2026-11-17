
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models
from routers.auth import router as auth_router


# Create FastAPI application
app = FastAPI(
    title="AI Document Assistant API",
    description="Authentication and AI Document Assistant API",
    version="1.0.0"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Class-Test"
    ]
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register authentication router
app.include_router(auth_router)


# Home API
@app.get("/")
def home():
    return {
        "message": "AI Document Assistant API is running"
    }


# Health check API
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
