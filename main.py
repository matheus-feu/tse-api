import sys
from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from alembic import command
from app.api.v1 import tse_results_etl_routes, votation_routes, ckan_routes, tse_packages_routes
from app.core.config import settings
from app.core.database import init_db, create_database_if_not_exists

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/app_{time}.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de contexto para o ciclo de vida da aplicação FastAPI."""
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")

    await create_database_if_not_exists()
    logger.info("✅ Banco de dados verificado/criado")

    await init_db()
    logger.info("✅ Banco de dados inicializado")

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("✅ Migrations aplicadas!")

    yield
    logger.info("👋 Encerrando aplicação...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para extração e processamento de dados eleitorais do TSE",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tse_results_etl_routes.router, prefix="/api/v1", tags=["ETL Candidato/Partido - TSE"])
app.include_router(votation_routes.router, prefix="/api/v1", tags=["Apuração - TSE"])
app.include_router(tse_packages_routes.router, prefix="/api/v1", tags=["ETL Packages - TSE"])
app.include_router(ckan_routes.router, prefix="/api/v1", tags=["CKAN - TSE"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
