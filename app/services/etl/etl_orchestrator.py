import uuid
from typing import Optional, Dict, List

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.log_repository import ETLLogRepository
from app.services.etl.extractors.votation_candidate_extractor import VotationExtractor
from app.services.etl.loaders.votation_loader import VotationLoader
from app.services.etl.transformers.votation_transformer import (
    VotationPartyTransformer,
    VotationCandidateTransformer
)


class ETLOrchestrator:
    """Orquestra Extract → Transform → Load com logging."""

    def __init__(self, db_session: AsyncSession, batch_size: int = 1000):
        """
        Inicializa o orquestrador do ETL.

        Args:
            db_session: Sessão do banco de dados
            batch_size: Tamanho do batch para inserção
        """
        self.extractor = VotationExtractor()
        self.transformer_candidate = VotationCandidateTransformer()
        self.transformer_partido = VotationPartyTransformer()
        self.loader = VotationLoader(db_session)
        self.log_repo = ETLLogRepository(db_session)
        self.batch_size = batch_size

    async def _process_chunks(self, records: List[Dict], loader_method) -> int:
        """Processa registros em chunks e retorna total carregado."""
        chunks = [
            records[i:i + self.batch_size]
            for i in range(0, len(records), self.batch_size)
        ]

        total_loaded = 0
        for chunk in chunks:
            loaded = await loader_method(chunk)
            total_loaded += loaded
            logger.debug(f"💾 Chunk: {loaded:,} registros (total: {total_loaded:,})")

        return total_loaded

    async def _run_etl(
            self,
            process_type: str,
            year: int,
            extractor_method,
            transformer_method,
            loader_method,
            uf: Optional[str] = None,
            log_id: Optional[uuid.UUID] = None
    ) -> str:
        """Template genérico para ETL com logging."""
        process_name = f"etl_votacao_{process_type}_{year}_{uf or 'BRASIL'}"
        total_loaded = 0

        try:
            logger.info(f"🚀 ETL iniciado: {process_name} [Log ID: {log_id}]")
            await self.log_repo.update_log_progress(log_id, 'PROCESSANDO', 0)

            # Extract & Transform & Load
            async for df in extractor_method(year=year, uf=uf):
                # Transform
                await self.log_repo.update_log_progress(log_id, 'TRANSFORMANDO')
                records = transformer_method(df)

                # Load
                await self.log_repo.update_log_progress(log_id, 'CARREGANDO')
                loaded = await self._process_chunks(records, loader_method)
                total_loaded += loaded

                logger.info(f"💾 {loaded:,} salvos (total: {total_loaded:,})")

            await self.log_repo.finalize_log(log_id, 'SUCESSO', total_loaded, None)
            logger.info(f"✅ {process_name} concluído: {total_loaded:,} registros")
            return str(log_id)

        except Exception as e:
            await self.log_repo.finalize_log(log_id, 'ERRO', total_loaded, str(e)[:500])
            logger.error(f"❌ Erro em {process_name}: {e}", exc_info=True)
            raise

        finally:
            await self.extractor.close()

    async def run_etl_votation_candidate(self, year: int, log_id: uuid.UUID, uf: Optional[str] = None, ) -> str:
        """ETL de votação por candidato."""
        return await self._run_etl(
            process_type='candidato',
            year=year,
            uf=uf,
            log_id=log_id,
            extractor_method=self.extractor.extract_votation_year,
            transformer_method=self.transformer_candidate.transform_dataframe_in_dict,
            loader_method=self.loader.load_candidates
        )

    async def run_etl_votation_partido(self, year: int, log_id: uuid.UUID, uf: Optional[str] = None) -> str:
        """ETL de votação por partido."""
        return await self._run_etl(
            process_type='partido',
            year=year,
            uf=uf,
            log_id=log_id,
            extractor_method=self.extractor.extract_votation_year,
            transformer_method=self.transformer_partido.transform_dataframe_in_dict,
            loader_method=self.loader.load_parties
        )

    async def __aenter__(self):
        """Context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - fecha recursos."""
        await self.extractor.close()
