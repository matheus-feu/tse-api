from datetime import datetime
from typing import List, Optional

from loguru import logger
from sqlalchemy import select, func, and_, desc
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

    # =========================================================================
    # OPERAÇÕES DE CRIAÇÃO E ATUALIZAÇÃO
    # =========================================================================

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
            log.error_message = error_message[:500]  # Trunca se for muito grande

        await self.session.commit()
        await self.session.refresh(log)

        duration = (log.end_time - log.start_time).total_seconds()
        logger.info(
            f"📝 Log finalizado: {log.id} - Status: {status} - "
            f"Registros: {records_processed} - Duração: {duration:.2f}s"
        )

        return log

    # =========================================================================
    # CONSULTAS
    # =========================================================================

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

    async def find_recent(
            self,
            process_name: Optional[str] = None,
            status: Optional[str] = None,
            limite: int = 50
    ) -> List[ETLLog]:
        """
        Busca logs recentes com filtros.

        Args:
            process_name: Filtrar por nome do processo (busca parcial)
            status: Filtrar por status
            limite: Limite de resultados

        Returns:
            Lista de logs
        """
        stmt = select(ETLLog)

        conditions = []
        if process_name:
            conditions.append(ETLLog.process_name.ilike(f"%{process_name}%"))
        if status:
            conditions.append(ETLLog.status == status)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(desc(ETLLog.start_time)).limit(limite)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_by_package(self, package_id: str) -> List[ETLLog]:
        """
        Busca logs relacionados a um package CKAN.

        Args:
            package_id: ID do package CKAN

        Returns:
            Lista de logs
        """
        stmt = select(ETLLog).where(
            ETLLog.package_id == package_id
        ).order_by(desc(ETLLog.start_time))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_last_success(self, process_name: str) -> Optional[ETLLog]:
        """
        Busca última execução bem-sucedida de um processo.

        Args:
            process_name: Nome do processo

        Returns:
            Último log com sucesso ou None
        """
        stmt = select(ETLLog).where(
            and_(
                ETLLog.process_name == process_name,
                ETLLog.status == 'SUCESSO'
            )
        ).order_by(desc(ETLLog.end_time)).limit(1)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # =========================================================================
    # ESTATÍSTICAS
    # =========================================================================

    async def get_stats(self) -> dict:
        """
        Retorna estatísticas gerais dos logs.

        Returns:
            Dicionário com estatísticas
        """
        stmt = select(
            func.count(ETLLog.id).label('total'),
            func.count(ETLLog.id).filter(ETLLog.status == 'SUCESSO').label('sucessos'),
            func.count(ETLLog.id).filter(ETLLog.status == 'ERRO').label('erros'),
            func.count(ETLLog.id).filter(ETLLog.status == 'INICIADO').label('em_andamento'),
            func.sum(ETLLog.records_processed).label('total_registros')
        )

        result = await self.session.execute(stmt)
        stats = result.one()

        return {
            'total_execucoes': stats.total or 0,
            'sucessos': stats.sucessos or 0,
            'erros': stats.erros or 0,
            'em_andamento': stats.em_andamento or 0,
            'total_registros_processados': stats.total_registros or 0
        }

    async def count_by_status(self) -> dict:
        """
        Conta logs agrupados por status.

        Returns:
            Dicionário com contagens por status
        """
        stmt = select(
            ETLLog.status,
            func.count(ETLLog.id).label('count')
        ).group_by(ETLLog.status)

        result = await self.session.execute(stmt)
        rows = result.all()

        return {row.status: row.count for row in rows}

    # =========================================================================
    # LIMPEZA
    # =========================================================================

    async def delete_old_logs(self, days: int = 30) -> int:
        """
        Remove logs antigos (útil para manutenção).

        Args:
            days: Manter logs dos últimos N dias

        Returns:
            Número de logs removidos
        """
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        stmt = select(ETLLog).where(ETLLog.start_time < cutoff_date)
        result = await self.session.execute(stmt)
        logs_to_delete = result.scalars().all()

        for log in logs_to_delete:
            await self.session.delete(log)

        await self.session.commit()

        logger.info(f"🗑️  Removidos {len(logs_to_delete)} logs antigos (>{days} dias)")
        return len(logs_to_delete)
