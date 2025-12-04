import uuid
from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.etl_log import ETLLog


class ETLLogRepository:
    """Repository para operações de log de ETL."""

    def __init__(self, session: AsyncSession):
        """
        Inicializa o repository.

        Args:
            session: Sessão assíncrona do SQLAlchemy
        """
        self.session = session

    async def create_log(self, process_name: str) -> ETLLog:
        """
        Cria novo log de ETL com status pending.
        process_name: Nome do processo (ex: "etl_candidato_2024_SP")
        """
        log = ETLLog(
            process_name=process_name,
            status='pending',
            start_time=datetime.utcnow()
        )

        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)

        logger.info(f"📝 Log criado: {log.id} - {process_name}")
        return log

    async def get(self, log_id: uuid.UUID) -> Optional[ETLLog]:
        """
        Recupera um ETLLog pelo ID.
        Args:
            log_id: ID do log (UUID)
        """
        res = await self.session.execute(
            select(ETLLog).where(ETLLog.id == log_id)
        )
        return res.scalar_one_or_none()

    async def mark_pending(self, log_id: uuid.UUID) -> None:
        """
        Marca o log como pendente.
        """
        log = await self.get(log_id)
        if log:
            log.status = "pending"
            await self.session.commit()

    async def mark_processing(self, log_id: uuid.UUID) -> None:
        """
        Marca o log como em processamento.
        """
        log = await self.get(log_id)
        if log:
            log.status = "processing"
            await self.session.commit()

    async def mark_done(self, log_id: uuid.UUID, records_processed: int) -> None:
        """
        Marca o log como concluído.
        """
        log = await self.get(log_id)
        if log:
            log.status = "done"
            log.end_time = datetime.utcnow()
            log.records_processed = records_processed
            await self.session.commit()

    async def mark_error(self, log_id: uuid.UUID, error_message: str) -> None:
        """
        Marca o log como erro.
        """
        log = await self.get(log_id)
        if log:
            log.status = "error"
            log.end_time = datetime.utcnow()
            log.error_message = error_message
            await self.session.commit()
