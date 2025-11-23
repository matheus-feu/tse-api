from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db_session() -> AsyncSession:
    """
    Dependency que fornece sessão do banco.
    Uso: db: AsyncSession = Depends(get_db_session)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Inicializa o banco de dados (cria tabelas se necessário)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
