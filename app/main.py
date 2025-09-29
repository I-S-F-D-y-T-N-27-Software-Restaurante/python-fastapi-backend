import logging

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import SQLAlchemyError

from app.config import HOST, PORT
from app.default.routes import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    server = FastAPI(title="Restorant Backend API")
    server.include_router(api_router, prefix="/api")

    @server.get("/favicon.ico")
    async def favicon():
        return Response(status_code=204)

    @server.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(_request: Request, exc: SQLAlchemyError):
        logger.error("Database error: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error while accessing the database"},
        )

    @server.exception_handler(Exception)
    async def global_exception_handler(_request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return server


app = create_app()

# if __name__ == "__main__":
#     try:
#         uvicorn.run(
#             "app.main:app",
#             host=HOST,
#             port=PORT,
#             reload=True,
#         )
#     except OSError as e:
#         logger.critical("OS error while starting server: %s", e, exc_info=True)
#     except KeyboardInterrupt:
#         logger.info("Server stopped by user")
