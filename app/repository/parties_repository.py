from typing import List, Optional, Dict

from loguru import logger
from sqlalchemy import select, func, and_
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

    # =========================================================================
    # CONSULTAS BÁSICAS
    # =========================================================================

    async def find_by_filters(
            self, ano: Optional[int] = None, uf: Optional[str] = None,
            municipio: Optional[str] = None, zona: Optional[int] = None,
            partido: Optional[str] = None, cargo: Optional[str] = None,
            limite: int = 100, offset: int = 0
    ) -> List[VotoPartidoMunZona]:
        """Busca com filtros."""
        stmt = select(VotoPartidoMunZona)

        conditions = []
        if ano: conditions.append(VotoPartidoMunZona.ano_eleicao == ano)
        if uf: conditions.append(VotoPartidoMunZona.sg_uf == uf.upper())
        if municipio: conditions.append(VotoPartidoMunZona.nm_municipio.ilike(f"%{municipio}%"))
        if zona: conditions.append(VotoPartidoMunZona.nr_zona == zona)
        if partido: conditions.append(VotoPartidoMunZona.sg_partido == partido.upper())
        if cargo: conditions.append(VotoPartidoMunZona.ds_cargo.ilike(f"%{cargo}%"))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(limite).offset(offset).order_by(
            VotoPartidoMunZona.ano_eleicao.desc(),
            VotoPartidoMunZona.qt_votos_nominais.desc()
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    # =========================================================================
    # ESTATÍSTICAS
    # =========================================================================

    async def get_estatisticas(self, ano: int, uf: str) -> Dict:
        """Estatísticas agregadas."""
        stmt = select(
            func.count(VotoPartidoMunZona.id).label('total_registros'),
            func.sum(VotoPartidoMunZona.qt_votos_nominais).label('total_votos'),
            func.sum(VotoPartidoMunZona.qt_votos_nominais_validos).label('total_votos_validos'),
            func.sum(VotoPartidoMunZona.qt_votos_nominais_anulados).label('total_votos_anulados'),
            func.count(func.distinct(VotoPartidoMunZona.nr_zona)).label('total_zonas'),
            func.count(func.distinct(VotoPartidoMunZona.cd_municipio)).label('total_municipios'),
            func.count(func.distinct(VotoPartidoMunZona.nr_partido)).label('total_partidos')
        ).where(
            and_(
                VotoPartidoMunZona.ano_eleicao == ano,
                VotoPartidoMunZona.sg_uf == uf.upper()
            )
        )

        result = await self.session.execute(stmt)
        stats = result.one()

        return {
            'ano': ano, 'uf': uf.upper(),
            'total_registros': stats.total_registros or 0,
            'total_votos': stats.total_votos or 0,
            'total_votos_validos': stats.total_votos_validos or 0,
            'total_votos_anulados': stats.total_votos_anulados or 0,
            'total_zonas': stats.total_zonas or 0,
            'total_municipios': stats.total_municipios or 0,
            'total_partidos': stats.total_partidos or 0
        }

    async def get_ranking_partidos(self, ano: int, uf: str, limite: int = 10) -> List[Dict]:
        """Ranking dos partidos mais votados."""
        stmt = select(
            VotoPartidoMunZona.nr_partido,
            VotoPartidoMunZona.sg_partido,
            VotoPartidoMunZona.nm_partido,
            func.sum(VotoPartidoMunZona.qt_votos_nominais).label('total_votos')
        ).where(
            and_(
                VotoPartidoMunZona.ano_eleicao == ano,
                VotoPartidoMunZona.sg_uf == uf.upper()
            )
        ).group_by(
            VotoPartidoMunZona.nr_partido,
            VotoPartidoMunZona.sg_partido,
            VotoPartidoMunZona.nm_partido
        ).order_by(
            func.sum(VotoPartidoMunZona.qt_votos_nominais).desc()
        ).limit(limite)

        result = await self.session.execute(stmt)

        return [
            {
                'posicao': idx + 1,
                'nr_partido': row.nr_partido,
                'sg_partido': row.sg_partido,
                'nm_partido': row.nm_partido,
                'total_votos': row.total_votos
            }
            for idx, row in enumerate(result.all())
        ]
