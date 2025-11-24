from typing import List, Dict

from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parties import VotoPartidoMunZona


class PartiesRepository:
    """Repository para votação por partido - versão otimizada."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_upsert_votes(self, votacoes: List[Dict]) -> int:
        """
        UPSERT em massa - operação principal do ETL.
        Insere novos ou atualiza existentes baseado na constraint de unicidade.
        """
        if not votacoes:
            logger.warning("Lista vazia - nenhum registro para processar")
            return 0

        try:
            stmt = insert(VotoPartidoMunZona).values(votacoes)

            # Constraint: ano, uf, municipio, zona, turno, partido, cargo
            stmt = stmt.on_conflict_do_update(
                index_elements=['ano_eleicao', 'sg_uf', 'cd_municipio', 'nr_zona',
                                'nr_turno', 'nr_partido', 'cd_cargo'],
                set_={
                    'qt_votos_nominais': stmt.excluded.qt_votos_nominais,
                    'qt_votos_nominais_validos': stmt.excluded.qt_votos_nominais_validos,
                    'qt_votos_nominais_anulados': stmt.excluded.qt_votos_nominais_anulados,
                    'endereco_zona': stmt.excluded.endereco_zona,
                    'bairro_zona': stmt.excluded.bairro_zona,
                    'cep_zona': stmt.excluded.cep_zona,
                    'telefone_zona': stmt.excluded.telefone_zona,
                    'zona_eleitoral_id': stmt.excluded.zona_eleitoral_id,
                }
            )

            await self.session.execute(stmt)
            await self.session.commit()

            logger.info(f"✅ Upsert: {len(votacoes)} registros de partido")
            return len(votacoes)

        except Exception as e:
            await self.session.rollback()
            logger.error(f"❌ Erro no bulk_upsert: {e}")
            raise
