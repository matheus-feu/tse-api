import asyncio
from datetime import datetime
from typing import Optional, Dict

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.log_repository import ETLLogRepository
from app.services.etl.extractors.votation_candidate_extractor import VotacaoCandidatoExtractor
from app.services.etl.loaders.votacao_loader import VotationLoader
from app.services.etl.transformers.votacao_transformer import (
    VotationPartyTransformer,
    VotationCandidateTransformer
)


class ETLOrchestrator:
    """Orquestra Extract → Transform → Load com logging."""

    def __init__(self, db_session: AsyncSession, batch_size: int = 5000):
        """
        Inicializa o orquestrador.

        Args:
            db_session: Sessão do banco de dados
            batch_size: Tamanho do batch para inserção
        """
        # Componentes ETL
        self.extractor = VotacaoCandidatoExtractor()
        self.transformer_candidate = VotationCandidateTransformer()
        self.transformer_partido = VotationPartyTransformer()
        self.loader = VotationLoader(db_session)

        # Repository de logs
        self.log_repo = ETLLogRepository(db_session)

        # Configurações
        self.batch_size = batch_size

    async def run_etl_votation_candidate(self, ano: int, uf: Optional[str] = None) -> str:
        """ETL com processamento paralelo de batches."""
        process_name = f"etl_candidato_{ano}_{uf or 'BR'}"
        log = await self.log_repo.create_log(process_name=process_name)

        total_loaded = 0

        try:
            logger.info(f"🚀 ETL iniciado: {process_name}")
            await self.log_repo.update_log_progress(log.id, 'PROCESSANDO', 0)

            async for df in self.extractor.extract_votation_year(year=ano, uf=uf):
                # Transform
                records = self.transformer_candidate.transform_dataframe_in_dict(df)

                # Load em chunks para evitar sobrecarga de memória
                chunks = [records[i:i + self.batch_size] for i in range(0, len(records), self.batch_size)]

                # Processa os chunks em paralelo
                for chunk in chunks:
                    loaded = await self.loader.load_candidates(chunk)
                    total_loaded += loaded

                    logger.info(f"💾 {loaded:,} salvos (total: {total_loaded:,})")

                await self.log_repo.update_log_progress(log.id, 'CARREGANDO', total_loaded)

            await self.log_repo.finalize_log(log.id, 'SUCESSO', total_loaded, None)
            logger.info(f"✅ Concluído: {total_loaded:,} registros")

            return str(log.id)

        except Exception as e:
            await self.log_repo.finalize_log(log.id, 'ERRO', total_loaded, str(e)[:500])
            logger.error(f"❌ Erro: {e}", exc_info=True)
            raise

        finally:
            await self.extractor.close()

    async def run_etl_votacao_partido(
            self,
            ano: int,
            uf: Optional[str] = None,
    ) -> Dict:
        """
        🎯 ETL completo para votação por partido COM LOGS.
        Fluxo idêntico ao candidato, mas usa transformer e loader de partido.
        """
        # CRIAR LOG
        processo = f"etl_partido_{ano}_{uf or 'BR'}"
        log = await self.log_repo.create_log(process_name=processo)

        logger.info(f"🚀 ETL Partido: {processo} [Log ID: {log.id}]")

        stats = {
            'log_id': str(log.id),
            'tipo': 'votacao_partido',
            'inicio': datetime.utcnow(),
            'ano': ano,
            'uf': uf,
            'extraidos': 0,
            'transformados': 0,
            'carregados': 0,
            'status': 'INICIADO'
        }

        batch = []

        try:
            # EXTRACT
            await self.log_repo.update_log_progress(log.id, 'EXTRAINDO')
            logger.info("📥 FASE 1: EXTRACT")

            async for df in self.extractor.extract_votacao_partido_ano(ano, uf):
                stats['extraidos'] += len(df)

                if stats['extraidos'] % 10000 == 0:
                    await self.log_repo.update_log_progress(
                        log.id, 'EXTRAINDO', stats['extraidos']
                    )

                # TRANSFORM
                await self.log_repo.update_log_progress(log.id, 'TRANSFORMANDO')
                logger.info("🔄 FASE 2: TRANSFORM")
                records = self.transformer_partido.transform_dataframe(df)
                stats['transformados'] += len(records)

                batch.extend(records)

                # LOAD
                if len(batch) >= self.batch_size:
                    await self.log_repo.update_log_progress(log.id, 'CARREGANDO')
                    logger.info(f"💾 FASE 3: LOAD - {len(batch)} registros")
                    loaded = await self.loader.load_partidos(batch)
                    stats['carregados'] += loaded
                    batch = []

            # Último batch
            if batch:
                loaded = await self.loader.load_partidos(batch)
                stats['carregados'] += loaded

            # FINALIZAÇÃO
            stats['fim'] = datetime.utcnow()
            stats['duracao'] = (stats['fim'] - stats['inicio']).total_seconds()
            stats['status'] = 'SUCESSO'

            await self.log_repo.finalize_log(
                log.id, 'SUCESSO', stats['carregados']
            )

            logger.info(
                f"✅ ETL Partido concluído: {stats['carregados']} registros "
                f"em {stats['duracao']:.2f}s [Log ID: {log.id}]"
            )
            return stats

        except Exception as e:
            stats['status'] = 'ERRO'
            stats['erro'] = str(e)

            await self.log_repo.finalize_log(
                log.id, 'ERRO', stats['carregados'], str(e)[:500]
            )

            logger.error(f"❌ Erro no ETL Partido [Log ID: {log.id}]: {e}")
            raise
        finally:
            await self.extractor.close()
