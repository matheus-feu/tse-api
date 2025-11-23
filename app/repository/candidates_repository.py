from typing import List, Optional, Sequence, Dict

from loguru import logger
from sqlalchemy import select, delete, func, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidates import VotoCandidatoMunZona


class CandidatesRepository:
    """Repositório para operações de banco de dados relacionadas a votos de candidatos por município e zona."""

    def __init__(self, db_session: AsyncSession):
        """
        Inicializa o repository.

        Args:
            db_session: Sessão assíncrona do SQLAlchemy
        """
        self.db_session = db_session

    # =========================================================================
    # MÉTODOS DE CONSULTA
    # =========================================================================

    async def get_votes_by_candidate(
            self,
            candidate_number: int,
            state: Optional[str] = None
    ) -> Sequence[VotoCandidatoMunZona]:
        """
        Recupera votos de um candidato específico, opcionalmente filtrando por estado.

        Args:
            candidate_number: Número do candidato
            state: Sigla do estado (opcional)

        Returns:
            Lista de registros de votação
        """
        logger.info(f"Buscando votos do candidato {candidate_number}, estado: {state or 'TODOS'}")

        query = select(VotoCandidatoMunZona).where(
            VotoCandidatoMunZona.nr_candidato == candidate_number
        )

        if state:
            query = query.where(VotoCandidatoMunZona.sg_uf == state.upper())

        result = await self.db_session.execute(query)
        votos = result.scalars().all()

        logger.info(f"Encontrados {len(votos)} registros de votação")
        return votos

    async def find_by_filters(
            self,
            ano: Optional[int] = None,
            uf: Optional[str] = None,
            municipio: Optional[str] = None,
            zona: Optional[int] = None,
            candidato: Optional[str] = None,
            partido: Optional[str] = None,
            cargo: Optional[str] = None,
            turno: Optional[int] = None,
            limite: int = 100,
            offset: int = 0
    ) -> Sequence[VotoCandidatoMunZona]:
        """
        Busca votações com múltiplos filtros.

        Args:
            ano: Ano da eleição
            uf: Sigla da UF
            municipio: Nome do município (busca parcial)
            zona: Número da zona eleitoral
            candidato: Nome do candidato (busca parcial)
            partido: Sigla do partido
            cargo: Descrição do cargo
            turno: Número do turno
            limite: Limite de resultados
            offset: Offset para paginação

        Returns:
            Lista de votações encontradas
        """
        logger.info(f"Buscando votos com filtros: ano={ano}, uf={uf}, municipio={municipio}, zona={zona}")

        stmt = select(VotoCandidatoMunZona)

        # Aplica filtros
        conditions = []
        if ano:
            conditions.append(VotoCandidatoMunZona.ano_eleicao == ano)
        if uf:
            conditions.append(VotoCandidatoMunZona.sg_uf == uf.upper())
        if municipio:
            conditions.append(VotoCandidatoMunZona.nm_municipio.ilike(f"%{municipio}%"))
        if zona:
            conditions.append(VotoCandidatoMunZona.nr_zona == zona)
        if candidato:
            conditions.append(VotoCandidatoMunZona.nm_candidato.ilike(f"%{candidato}%"))
        if partido:
            conditions.append(VotoCandidatoMunZona.sg_partido == partido.upper())
        if cargo:
            conditions.append(VotoCandidatoMunZona.ds_cargo.ilike(f"%{cargo}%"))
        if turno:
            conditions.append(VotoCandidatoMunZona.nr_turno == turno)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(limite).offset(offset).order_by(
            VotoCandidatoMunZona.ano_eleicao.desc(),
            VotoCandidatoMunZona.qt_votos_nominais.desc()
        )

        result = await self.db_session.execute(stmt)
        votos = result.scalars().all()

        logger.info(f"Encontrados {len(votos)} registros com os filtros aplicados")
        return votos

    async def find_by_id(self, voto_id: str) -> Optional[VotoCandidatoMunZona]:
        """
        Busca votação por ID.

        Args:
            voto_id: ID da votação (UUID)

        Returns:
            Votação encontrada ou None
        """
        logger.debug(f"Buscando votação por ID: {voto_id}")

        stmt = select(VotoCandidatoMunZona).where(VotoCandidatoMunZona.id == voto_id)
        result = await self.db_session.execute(stmt)
        voto = result.scalar_one_or_none()

        if voto:
            logger.debug(f"Votação encontrada: {voto}")
        else:
            logger.warning(f"Votação não encontrada para ID: {voto_id}")

        return voto

    # =========================================================================
    # MÉTODOS DE INSERÇÃO
    # =========================================================================

    async def add_vote_record(self, vote_record: VotoCandidatoMunZona) -> None:
        """
        Adiciona um novo registro de voto para um candidato.

        Args:
            vote_record: Objeto VotoCandidatoMunZona
        """
        logger.info(f"Adicionando registro de voto: candidato {vote_record.nr_candidato}")

        try:
            self.db_session.add(vote_record)
            await self.db_session.commit()
            await self.db_session.refresh(vote_record)
            logger.info(f"Registro adicionado com sucesso: ID {vote_record.id}")
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro ao adicionar registro de voto: {e}")
            raise

    async def bulk_insert_votes(self, vote_records: List[dict]) -> None:
        """
        Insere múltiplos registros de votos em massa.
        Não faz UPSERT - gera erro se houver duplicatas.

        Args:
            vote_records: Lista de dicionários com dados de votação
        """
        if not vote_records:
            logger.warning("Lista de votos vazia, nenhum registro para inserir")
            return

        logger.info(f"Iniciando bulk insert de {len(vote_records)} registros")

        try:
            stmt = insert(VotoCandidatoMunZona).values(vote_records)
            await self.db_session.execute(stmt)
            await self.db_session.commit()
            logger.info(f"Bulk insert de {len(vote_records)} registros concluído com sucesso")
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
            logger.warning("Lista de votos vazia, nenhum registro para processar")
            return 0

        logger.info(f"Iniciando bulk upsert de {len(vote_records)} registros")

        try:
            stmt = insert(VotoCandidatoMunZona).values(vote_records)

            # Define atualização em caso de conflito
            # Baseado na constraint: ano_eleicao, sg_uf, cd_municipio, nr_zona, nr_turno, nr_candidato
            stmt = stmt.on_conflict_do_update(
                index_elements=[
                    'ano_eleicao', 'sg_uf', 'cd_municipio', 'nr_zona',
                    'nr_turno', 'nr_candidato'
                ],
                set_={
                    'cd_eleicao': stmt.excluded.cd_eleicao,
                    'dt_eleicao': stmt.excluded.dt_eleicao,
                    'sg_ue': stmt.excluded.sg_ue,
                    'nm_ue': stmt.excluded.nm_ue,
                    'nm_municipio': stmt.excluded.nm_municipio,
                    'ds_cargo': stmt.excluded.ds_cargo,
                    'nm_candidato': stmt.excluded.nm_candidato,
                    'nm_social_candidato': stmt.excluded.nm_social_candidato,
                    'nr_partido': stmt.excluded.nr_partido,
                    'sg_partido': stmt.excluded.sg_partido,
                    'nm_partido': stmt.excluded.nm_partido,
                    'qt_votos_nominais': stmt.excluded.qt_votos_nominais,
                    'qt_votos_nominais_validos': stmt.excluded.qt_votos_nominais_validos,
                    'endereco_zona': stmt.excluded.endereco_zona,
                    'bairro_zona': stmt.excluded.bairro_zona,
                    'cep_zona': stmt.excluded.cep_zona,
                    'telefone_zona': stmt.excluded.telefone_zona,
                    'zona_eleitoral_id': stmt.excluded.zona_eleitoral_id,
                }
            )

            result = await self.db_session.execute(stmt)
            await self.db_session.commit()

            logger.info(f"Bulk upsert de {len(vote_records)} registros concluído com sucesso")
            return len(vote_records)

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro no bulk_upsert_votes: {e}")
            raise

    # =========================================================================
    # MÉTODOS DE CONTAGEM
    # =========================================================================

    async def count_votes_by_candidate(self, candidate_number: int) -> int:
        """
        Conta o número de registros de votos para um candidato específico.

        Args:
            candidate_number: Número do candidato

        Returns:
            Total de registros
        """
        logger.debug(f"Contando votos do candidato {candidate_number}")

        query = select(func.count()).select_from(VotoCandidatoMunZona).where(
            VotoCandidatoMunZona.nr_candidato == candidate_number
        )
        result = await self.db_session.execute(query)
        total = result.scalar_one()

        logger.info(f"Candidato {candidate_number} possui {total} registros")
        return total

    async def count_by_filters(
            self,
            ano: Optional[int] = None,
            uf: Optional[str] = None,
            municipio: Optional[str] = None,
            zona: Optional[int] = None
    ) -> int:
        """
        Conta registros com filtros.

        Args:
            ano: Ano da eleição
            uf: Sigla da UF
            municipio: Nome do município
            zona: Número da zona

        Returns:
            Total de registros
        """
        logger.debug(f"Contando registros com filtros: ano={ano}, uf={uf}, municipio={municipio}, zona={zona}")

        stmt = select(func.count(VotoCandidatoMunZona.id))

        conditions = []
        if ano:
            conditions.append(VotoCandidatoMunZona.ano_eleicao == ano)
        if uf:
            conditions.append(VotoCandidatoMunZona.sg_uf == uf.upper())
        if municipio:
            conditions.append(VotoCandidatoMunZona.nm_municipio.ilike(f"%{municipio}%"))
        if zona:
            conditions.append(VotoCandidatoMunZona.nr_zona == zona)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db_session.execute(stmt)
        total = result.scalar()

        logger.info(f"Total de registros encontrados: {total}")
        return total

    # =========================================================================
    # MÉTODOS DE EXCLUSÃO
    # =========================================================================

    async def delete_votes_by_candidate(self, candidate_number: int) -> None:
        """
        Deleta registros de votos para um candidato específico.

        Args:
            candidate_number: Número do candidato
        """
        logger.warning(f"Deletando todos os votos do candidato {candidate_number}")

        try:
            stmt = delete(VotoCandidatoMunZona).where(
                VotoCandidatoMunZona.nr_candidato == candidate_number
            )
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()

            logger.info(f"Deletados {result.rowcount} registros do candidato {candidate_number}")
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro ao deletar votos do candidato {candidate_number}: {e}")
            raise

    async def delete_by_ano_uf(self, ano: int, uf: str) -> int:
        """
        Remove votações de um ano e UF específicos.

        Args:
            ano: Ano da eleição
            uf: Sigla da UF

        Returns:
            Número de registros removidos
        """
        logger.warning(f"Deletando votos de {uf}/{ano}")

        try:
            stmt = delete(VotoCandidatoMunZona).where(
                and_(
                    VotoCandidatoMunZona.ano_eleicao == ano,
                    VotoCandidatoMunZona.sg_uf == uf.upper()
                )
            )
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()

            logger.info(f"Removidos {result.rowcount} registros de {uf}/{ano}")
            return result.rowcount

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro ao deletar votos de {uf}/{ano}: {e}")
            raise

    # =========================================================================
    # MÉTODOS DE ESTATÍSTICAS
    # =========================================================================

    async def get_estatisticas(self, ano: int, uf: str) -> Dict:
        """
        Retorna estatísticas de votação.

        Args:
            ano: Ano da eleição
            uf: Sigla da UF

        Returns:
            Dicionário com estatísticas
        """
        logger.info(f"Gerando estatísticas para {uf}/{ano}")

        try:
            stmt = select(
                func.count(VotoCandidatoMunZona.id).label('total_registros'),
                func.sum(VotoCandidatoMunZona.qt_votos_nominais).label('total_votos'),
                func.sum(VotoCandidatoMunZona.qt_votos_nominais_validos).label('total_votos_validos'),
                func.count(func.distinct(VotoCandidatoMunZona.nr_zona)).label('total_zonas'),
                func.count(func.distinct(VotoCandidatoMunZona.cd_municipio)).label('total_municipios'),
                func.count(func.distinct(VotoCandidatoMunZona.nr_candidato)).label('total_candidatos')
            ).where(
                and_(
                    VotoCandidatoMunZona.ano_eleicao == ano,
                    VotoCandidatoMunZona.sg_uf == uf.upper()
                )
            )

            result = await self.db_session.execute(stmt)
            stats = result.one()

            estatisticas = {
                'ano': ano,
                'uf': uf.upper(),
                'total_registros': stats.total_registros or 0,
                'total_votos': stats.total_votos or 0,
                'total_votos_validos': stats.total_votos_validos or 0,
                'total_zonas': stats.total_zonas or 0,
                'total_municipios': stats.total_municipios or 0,
                'total_candidatos': stats.total_candidatos or 0
            }

            logger.info(f"Estatísticas geradas: {estatisticas}")
            return estatisticas

        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {e}")
            raise

    async def get_ranking_candidatos(
            self,
            ano: int,
            uf: str,
            cargo: Optional[str] = None,
            limite: int = 10
    ) -> List[Dict]:
        """
        Retorna ranking dos candidatos mais votados.

        Args:
            ano: Ano da eleição
            uf: Sigla da UF
            cargo: Descrição do cargo (opcional)
            limite: Número de candidatos no ranking

        Returns:
            Lista com ranking dos candidatos
        """
        logger.info(f"Gerando ranking de candidatos para {uf}/{ano}, cargo: {cargo or 'TODOS'}")

        conditions = [
            VotoCandidatoMunZona.ano_eleicao == ano,
            VotoCandidatoMunZona.sg_uf == uf.upper()
        ]

        if cargo:
            conditions.append(VotoCandidatoMunZona.ds_cargo.ilike(f"%{cargo}%"))

        stmt = select(
            VotoCandidatoMunZona.nr_candidato,
            VotoCandidatoMunZona.nm_candidato,
            VotoCandidatoMunZona.sg_partido,
            VotoCandidatoMunZona.ds_cargo,
            func.sum(VotoCandidatoMunZona.qt_votos_nominais).label('total_votos')
        ).where(
            and_(*conditions)
        ).group_by(
            VotoCandidatoMunZona.nr_candidato,
            VotoCandidatoMunZona.nm_candidato,
            VotoCandidatoMunZona.sg_partido,
            VotoCandidatoMunZona.ds_cargo
        ).order_by(
            func.sum(VotoCandidatoMunZona.qt_votos_nominais).desc()
        ).limit(limite)

        result = await self.db_session.execute(stmt)
        rows = result.all()

        ranking = [
            {
                'posicao': idx + 1,
                'nr_candidato': row.nr_candidato,
                'nm_candidato': row.nm_candidato,
                'sg_partido': row.sg_partido,
                'ds_cargo': row.ds_cargo,
                'total_votos': row.total_votos
            }
            for idx, row in enumerate(rows)
        ]

        logger.info(f"Ranking gerado com {len(ranking)} candidatos")
        return ranking
