import uuid
from typing import Callable, Awaitable

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.log_repository import ETLLogRepository
from app.services.etl.extractors.package_extractor import PackageExtractor
from app.services.etl.loaders.candidates_loader import CandidatesLoader
from app.services.etl.loaders.parties_loader import PartiesLoader
from app.services.etl.transformers.votation_transformer import VotationPartyTransformer


class PackageOrchestrator:
    """
    Orquestra o ETL para um TSEPackage:
    - Extract: baixa ZIP e lê CSV
    - Load: salva cada linha como raw em tse_packages
    - Atualiza o ETLLog (create_log/update/finalize) ao longo do fluxo
    """

    def __init__(self, log_id: uuid.UUID, db_session: AsyncSession):
        self.db_session = db_session
        self.extractor = PackageExtractor()
        self.log_repo = ETLLogRepository(db_session)

        self.pipelines: dict[str, Callable[[pd.DataFrame, AsyncSession], Awaitable[int]]] = {
            "votacao_partido_munzona": self._pipeline_votacao_partido,
            "votacao_candidato_munzona": self._pipeline_votacao_candidato,
            "perfil_comparecimento_abstencao": self._pipeline_perfil_comparecimento,
            # adicionar novos aqui, sem criar novos endpoints
        }
        self.log_id = log_id

    async def run(self, *, url: str, package_type: str) -> int:
        try:
            await self.log_repo.mark_pending(self.log_id)
            df, csv_name = await self.extractor.extract_csv_from_zip(url)

            pipeline = self.pipelines.get(package_type)
            if not pipeline:
                raise ValueError(f"Pipeline desconhecida para package_type '{package_type}'")

            inserted: int = await pipeline(df, self.db_session)
            await self.log_repo.mark_done(self.log_id, records_processed=inserted)

            return inserted

        except Exception as e:
            await self.log_repo.mark_error(self.log_id, str(e))
            raise

    async def _pipeline_votacao_candidato(self, df: pd.DataFrame, db_session: AsyncSession) -> int:
        transformer = VotationPartyTransformer()
        records = transformer.transform(df)
        loader = CandidatesLoader(db_session)
        return await loader.load_candidates(records)

    async def _pipeline_votacao_partido(self, df: pd.DataFrame, db_session: AsyncSession) -> int:
        loader = PartiesLoader(db_session)
        transformer = VotationPartyTransformer()
        records = transformer.transform(df)
        return await loader.load_parties(records)

    async def _pipeline_perfil_comparecimento(self, df: pd.DataFrame, db_session: AsyncSession) -> int:
        return 0
