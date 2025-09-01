import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from app.api.routes import api_router
from app.core.dotenv import ConfigEnum, settings

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    fast_api_instance = FastAPI(title=settings.get(key=ConfigEnum.APP_TITLE))

    # Include API routes
    fast_api_instance.include_router(api_router, prefix="/api")

    @fast_api_instance.get("/favicon.ico")
    async def favicon():
        return Response(status_code=204)

    # Global exception handler
    @fast_api_instance.exception_handler(Exception)
    async def global_exception_handler(_request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return fast_api_instance


app = create_app()

if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.get(key=ConfigEnum.HOST),
            port=settings.get(key=ConfigEnum.PORT),
            reload=True,
        )
    except OSError as e:
        logger.critical("OS error while starting server: %s", e, exc_info=True)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
