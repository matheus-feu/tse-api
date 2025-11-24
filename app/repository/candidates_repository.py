from typing import List
from typing import cast

from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Column

from app.models.candidates import VotoCandidatoMunZona


class CandidatesRepository:
    """Repositório para operações de banco de dados relacionadas a votos de candidatos por município e zona."""

    def __init__(self, db_session: AsyncSession):
        """
        Inicializa o repository.
        """
        self.db_session = db_session

    async def bulk_insert_votes(self, vote_records: List[dict]) -> int:
        """
        Insere múltiplos registros de votos em massa.
        Não faz UPSERT - gera erro se houver duplicatas.

        Args:
            vote_records: Lista de dicionários com dados de votação
        """
        if not vote_records:
            logger.warning("Lista de votos vazia, nenhum registro para inserir")
            return 0

        logger.info(f"Iniciando bulk insert de {len(vote_records)} registros")

        try:
            stmt = insert(VotoCandidatoMunZona).values(vote_records)
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()

            return result.rowcount if result.rowcount is not None else len(vote_records)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro no bulk_insert_votes: {e}")
            raise

    async def bulk_upsert_votes(self, vote_records: List[dict]) -> int:
        """
        Insere ou atualiza múltiplos registros de votos em massa.
        Usa UPSERT do PostgreSQL baseado na constraint de unicidade.

        Constraint: ano_eleicao, sg_uf, cd_municipio, nr_zona, nr_turno, nr_candidato

        Args:
            vote_records: Lista de dicionários com dados de votação

        Returns:
            Número de registros processados
        """
        if not vote_records:
            return 0

        unique_fields = [
            'ano_eleicao', 'nr_turno', 'sg_uf', 'cd_municipio', 'nr_zona', 'nr_candidato'
        ]

        try:
            stmt = insert(VotoCandidatoMunZona).values(vote_records)

            # Para cada coluna da tabela, exceto as únicas, atualize com o valor do EXCLUDED
            update_cols = {
                cast(Column, c).name: getattr(stmt.excluded, cast(Column, c).name)
                for c in VotoCandidatoMunZona.__table__.columns
                if cast(Column, c).name not in unique_fields and cast(Column, c).name != 'id'
            }

            stmt = stmt.on_conflict_do_update(
                index_elements=unique_fields,
                set_=update_cols,
            )

            result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            return result.rowcount if result.rowcount else len(vote_records)

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"❌ Erro no bulk_upsert_votes: {e}")
            raise
