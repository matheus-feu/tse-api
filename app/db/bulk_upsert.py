from typing import List, Dict, Type

from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def bulk_upsert(
        session: AsyncSession,
        model: Type,
        vote_records: List[Dict],
        unique_fields: List[str],
        skip_update: List[str] = None
) -> int:
    """
    UPSERT genérico em qualquer tabela.
    Args:
        session: Sessão assíncrona
        model: Model SQLAlchemy (tabela)
        vote_records: Lista de dicionários com dados
        unique_fields: Campos que formam a constraint única
        skip_update: Campos que não devem ser atualizados (ex: 'id')
    Returns:
        Quantidade de registros processados
    """
    if not vote_records:
        logger.warning("Lista vazia - nenhum registro para processar")
        return 0

    skip_update = skip_update or ['id']

    try:
        stmt = insert(model).values(vote_records)
        update_cols = {
            c.name: getattr(stmt.excluded, c.name)
            for c in model.__table__.columns
            if c.name not in unique_fields and c.name not in skip_update
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=unique_fields,
            set_=update_cols,
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount if result.rowcount else len(vote_records)
    except Exception as e:
        await session.rollback()
        logger.error(f"❌ Erro no bulk_upsert para {model.__tablename__}: {e}")
        raise
