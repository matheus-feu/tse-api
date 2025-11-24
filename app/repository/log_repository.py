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

    async def create_log(
            self,
            process_name: str,
            package_id: Optional[str] = None,
            resource_id: Optional[str] = None
    ) -> ETLLog:
        """
        Cria novo log de ETL com status INICIADO.

        Args:
            process_name: Nome do processo (ex: "etl_candidato_2024_SP")
            package_id: ID do package CKAN (opcional)
            resource_id: ID do resource CKAN (opcional)

        Returns:
            ETLLog criado
        """
        log = ETLLog(
            process_name=process_name,
            package_id=package_id,
            resource_id=resource_id,
            status='INICIADO',
            start_time=datetime.utcnow()
        )

        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)

        logger.info(f"📝 Log criado: {log.id} - {process_name}")
        return log

    async def update_log_progress(
            self,
            log_id: str,
            status: str,
            records_processed: Optional[int] = None
    ) -> ETLLog:
        """
        Atualiza progresso do log (usado durante processamento).

        Args:
            log_id: ID do log (UUID)
            status: Novo status (ex: "EM_PROGRESSO", "EXTRAINDO", "TRANSFORMANDO")
            records_processed: Número de registros processados até agora

        Returns:
            ETLLog atualizado
        """
        stmt = select(ETLLog).where(ETLLog.id == log_id)
        result = await self.session.execute(stmt)
        log = result.scalar_one_or_none()

        if not log:
            raise ValueError(f"Log {log_id} não encontrado")

        log.status = status
        if records_processed is not None:
            log.records_processed = records_processed

        await self.session.commit()
        await self.session.refresh(log)

        logger.debug(f"📝 Log atualizado: {log.id} - Status: {status}")
        return log

    async def finalize_log(
            self,
            log_id: str,
            status: str,
            records_processed: int,
            error_message: Optional[str] = None
    ) -> ETLLog:
        """
        Finaliza log (SUCESSO ou ERRO).

        Args:
            log_id: ID do log
            status: Status final ("SUCESSO" ou "ERRO")
            records_processed: Total de registros processados
            error_message: Mensagem de erro (se houver)

        Returns:
            ETLLog finalizado
        """
        stmt = select(ETLLog).where(ETLLog.id == log_id)
        result = await self.session.execute(stmt)
        log = result.scalar_one_or_none()

        if not log:
            raise ValueError(f"Log {log_id} não encontrado")

        log.status = status
        log.end_time = datetime.utcnow()
        log.records_processed = records_processed
        if error_message:
            log.error_message = error_message[:500]

        await self.session.commit()
        await self.session.refresh(log)

        duration = (log.end_time - log.start_time).total_seconds()
        logger.info(
            f"📝 Log finalizado: {log.id} - Status: {status} - "
            f"Registros: {records_processed} - Duração: {duration:.2f}s"
        )

        return log

    async def find_by_id(self, log_id: str) -> Optional[ETLLog]:
        """
        Busca log por ID.

        Args:
            log_id: ID do log (UUID)

        Returns:
            ETLLog ou None se não encontrado
        """
        stmt = select(ETLLog).where(ETLLog.id == log_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
