"""
Main FastAPI application.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import logging

from .core.config import settings
from .core.database import init_db
from .api.v1.router import api_router


# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.ENABLE_SWAGGER_UI else None,
    redoc_url="/redoc" if settings.ENABLE_SWAGGER_UI else None,
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error"
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Initialize database
    init_db()
    logger.info("Database initialized")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down application")


# Health check endpoint
@app.get("/health", tags=["Health"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.ENABLE_SWAGGER_UI else None
    }


# Include API router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
