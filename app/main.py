from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import interns, tasks, mentors, progress
from app.services.openai_service import openai_service
from app.schemas import DocumentSummarizeRequest, DocumentSummarizeResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    description="API for managing intern onboarding process",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(interns.router)
app.include_router(tasks.router)
app.include_router(mentors.router)
app.include_router(progress.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Intern Onboarding API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/documents/summarize", response_model=DocumentSummarizeResponse, tags=["OpenAI"])
async def summarize_document(request: DocumentSummarizeRequest):
    """Summarize a document using OpenAI"""
    summary = await openai_service.summarize_document(
        document_text=request.document_text,
        max_length=request.max_length or 200
    )
    return DocumentSummarizeResponse(summary=summary)
