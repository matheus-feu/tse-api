from typing import AsyncGenerator

import asyncpg
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=False,
    pool_size=20,
    max_overflow=40,
    poolclass=NullPool,
)

AsyncSessionMaker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que fornece sessão do banco.
    Uso: db: AsyncSession = Depends(get_db_session)
    """
    async with AsyncSessionMaker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Inicializa o banco de dados (cria tabelas se necessário)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_database_if_not_exists():
    """Cria o banco de dados se não existir."""
    try:
        conn = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database='postgres'
        )
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            settings.DB_NAME
        )

        if not exists:
            await conn.execute(f'CREATE DATABASE {settings.DB_NAME}')
            logger.info(f"✅ Banco de dados '{settings.DB_NAME}' criado!")
        else:
            logger.info(f"ℹ️  Banco '{settings.DB_NAME}' já existe.")
        await conn.close()
    except Exception as e:
        logger.error(f"❌ Erro ao criar banco: {e}")
        raise
