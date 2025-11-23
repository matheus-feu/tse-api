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
from app.services.localization.localization_service import LocalizationService


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
        self.enrich_localization = LocalizationService()
        self.loader = VotationLoader(db_session)

        # Repository de logs
        self.log_repo = ETLLogRepository(db_session)

        # Configurações
        self.batch_size = batch_size

    async def run_etl_votation_candidate(self, ano: int, uf: Optional[str] = None) -> Dict:
        """
        🎯 ETL completo para votação por candidato COM LOGS.

        FLUXO:
        1. EXTRACT → Baixa dados da CDN TSE (ZIP/CSV)
        2. TRANSFORM → Limpa e valida dados
        3. ENRICH → Enriquece com localização (se ativo)
        4. LOAD → Salva no banco (UPSERT)

        Args:
            ano: Ano da eleição (ex: 2024)
            uf: Sigla da UF (ex: "SP") ou None para todas
            turno: Número do turno (1 ou 2)

        Returns:
            Estatísticas do processo com log_id
        """
        process_name = f"etl_candidato_{ano}_{uf or 'BR'}"
        log = await self.log_repo.create_log(process_name=process_name)

        logger.info(f"🚀 ETL Candidato: {process_name} [Log ID: {log.id}]")

        batch: list = []

        stats = {
            'log_id': log.id,
            'tipo': 'votacao_candidato',
            'inicio': datetime.utcnow(),
            'ano': ano,
            'uf': uf,
            'extraidos': 0,
            'transformados': 0,
            'enriquecidos': 0,
            'carregados': 0,
            'status': 'INICIADO'
        }

        try:
            await self.log_repo.update_log_progress(
                log_id=log.id,
                status='EXTRAINDO',
                records_processed=0
            )
            logger.info("📥 FASE 1: EXTRACT - Baixando dados do CKAN...")

            async for df in self.extractor.extract_votation_year(year=ano, uf=uf):
                stats['extraidos'] += len(df)
                logger.info(f"  ↳ Extraídos {len(df)} registros (total: {stats['extraidos']})")

                # Atualiza log a cada 10k registros
                if stats['extraidos'] % 10000 == 0:
                    await self.log_repo.update_log_progress(
                        log_id=log.id,
                        status='EXTRAINDO',
                        records_processed=stats['extraidos']
                    )

                logger.info("🔄 FASE 2: TRANSFORM - Limpando e validando...")
                await self.log_repo.update_log_progress(
                    log.id,
                    status='TRANSFORMANDO',
                    records_processed=stats['extraidos']
                )

                records = self.transformer_candidate.transform_dataframe(df)
                stats['transformados'] += len(records)
                logger.info(f"  ↳ Transformados {len(records)} registros (total: {stats['transformados']})")

                # Enriquecimento de localização
                await self.log_repo.update_log_progress(
                    log_id=log.id,
                    status='ENRIQUECENDO',
                    records_processed=stats['enriquecidos']
                )

                logger.info("🌍 Enriquecendo dados de localização...")
                enriched_records = await self.enrich_localization.enrich_lotes(records)
                stats['enriquecidos'] += len(records)
                logger.info(f"  ↳ Enriquecidos {len(enriched_records)} registros")

                batch.extend(records)

                if len(batch) >= self.batch_size:
                    logger.info(f"💾 FASE 3: LOAD - Salvando batch de {len(batch)} registros...")
                    loaded = await self.loader.load_candidates(batch)
                    stats['carregados'] += loaded

                    await self.log_repo.update_log_progress(
                        log.id,
                        status='CARREGANDO',
                        records_processed=stats['carregados']
                    )

                    logger.info(f"  ↳ Salvos {loaded} registros no banco")
                    logger.info(
                        f"📊 Progresso: {stats['extraidos']} extraídos | "
                        f"{stats['transformados']} transformados | "
                        f"{stats['carregados']} carregados"
                    )

                    batch = []

                if batch:
                    logger.info(f"💾 Salvando últimos {len(batch)} registros...")
                    loaded = await self.loader.load_candidates(batch)
                    stats['carregados'] += loaded

                stats['fim'] = datetime.utcnow()
                stats['duracao'] = (stats['fim'] - stats['inicio']).total_seconds()
                stats['status'] = 'SUCESSO'

                await self.log_repo.finalize_log(
                    log_id=log.id,
                    status='SUCESSO',
                    records_processed=stats['carregados'],
                    error_message=None
                )

                logger.info("=" * 70)
                logger.info("✅ ETL CANDIDATO CONCLUÍDO COM SUCESSO!")
                logger.info(f"   📊 Extraídos: {stats['extraidos']}")
                logger.info(f"   ✨ Transformados: {stats['transformados']}")
                logger.info(f"   💾 Carregados: {stats['carregados']}")
                logger.info(f"   ⏱️  Duração: {stats['duracao']:.2f}s")
                logger.info(f"   📝 Log ID: {log.id}")
                logger.info("=" * 70)

                return stats

        except Exception as e:
            stats['status'] = 'ERRO'
            stats['erro'] = str(e)

            await self.log_repo.finalize_log(
                log_id=log.id,
                status='ERRO',
                records_processed=stats['carregados'],
                error_message=str(e)[:500]
            )

            logger.error(f"❌ Erro no ETL Candidato [Log ID: {log.id}]: {e}", exc_info=True)
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
