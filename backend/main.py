import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.db.session import Base, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENV == "dev":  # dev convenience only
        Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Lekhamudra API", version="0.1.0", lifespan=lifespan)

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    if getattr(settings, "ENABLE_REQUEST_LOGGING", True):

        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            logger = logging.getLogger("request")
            logger.debug(f"Incoming {request.method} {request.url.path}")
            response = await call_next(request)
            logger.debug(
                f"Completed {request.method} {request.url.path} status={response.status_code}"
            )
            return response

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logging.getLogger("app").exception("Unhandled error")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app


app = create_app()
