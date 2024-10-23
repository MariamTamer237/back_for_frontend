import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings  # Assuming settings are already configured
from .logger import setup_logging
from .routers import actions_routers, lead_routers

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Set up logging based on the environment
if settings.environment == "production":
    log_level = "INFO"
    log_file = logs_dir / "app.log"
else:
    log_level = "DEBUG"
    log_file = logs_dir / "app_debug.log"

setup_logging(log_level, log_file)

logger = logging.getLogger(__name__)

# Conditionally set the docs and openapi URLs based on the environment
if settings.environment == "production":
    docs_url = None
    openapi_url = None
else:
    docs_url = "/docs"
    openapi_url = "/openapi.json"

# Define allowed CORS origins (localhost:3000)
origins = [
    "http://localhost:3000",  # Allow frontend running on localhost:3000
]

# Create FastAPI app instance with docs/openapi URLs conditional on the environment
app = FastAPI(title=settings.app_name, docs_url=docs_url, openapi_url=openapi_url)

# Add CORS middleware to allow connections from specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the routers for handling different routes
app.include_router(lead_routers.router)
app.include_router(actions_routers.router)

# Log environment information
logger.info(f"App started with environment: {settings.environment}")


# Main function to run the app
def main():
    logger.info("Exited")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.app_port)
