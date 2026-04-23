from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.posts import router as posts_router
from api.users import router as users_router
from api.locations import router as locations_router
from api.categories import router as categories_router
from api.comments import router as comments_router
from api.auth import router as auth_router
from core.logging_config import setup_logging
from core.config import settings


def create_app() -> FastAPI:
    setup_logging(
        log_file=settings.LOG_FILE,
        max_bytes=settings.LOG_MAX_BYTES,
        backup_count=settings.LOG_BACKUP_COUNT,
    )

    app = FastAPI(root_path='/api/v1')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(auth_router, tags=['Auth'])
    app.include_router(posts_router, tags=['Posts'])
    app.include_router(users_router, tags=['Users'])
    app.include_router(locations_router, tags=['Locations'])
    app.include_router(categories_router, tags=['Categories'])
    app.include_router(comments_router, tags=['Comments'])
    return app


app = create_app()
