import uuid

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repository.log_repository import ETLLogRepository
from app.schemas.etl_schemas import ETLResponse, ETLRequest, ETLLogResponse
from app.services.etl.etl_orchestrator import ETLOrchestrator

router = APIRouter()


@router.get("/etl/logs/{log_id}", response_model=ETLLogResponse)
async def get_status_job(log_id: str, db: AsyncSession = Depends(get_db_session)):
    """
    Consulta o status do job ETL pelo log_id retornado ao iniciar o processo ETL.
    """
    repo = ETLLogRepository(db)
    log = await repo.find_by_id(log_id)

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log '{log_id}' não encontrado"
        )

    return ETLLogResponse.from_orm(log)


@router.post("/etl/execute", response_model=ETLResponse)
async def execute_etl(
        request: ETLRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db_session)
):
    """Inicia ETL em background."""

    log_repo = ETLLogRepository(db)
    process_name = f"etl_{request.tipo}_{request.ano}_{request.uf}"
    log = await log_repo.create_log(process_name=process_name)

    async def run_etl_background_task(log_id: uuid.UUID):
        """Wrapper para executar ETL e fazer cleanup."""
        orchestrator = ETLOrchestrator(db_session=db, batch_size=1000)
        try:
            if request.tipo == "candidato":
                log_id = await orchestrator.run_etl_votation_candidate(
                    year=request.ano,
                    uf=request.uf,
                    log_id=log_id
                )
            elif request.tipo == "partido":
                log_id = await orchestrator.run_etl_votation_partido(
                    year=request.ano,
                    uf=request.uf,
                    log_id=log_id
                )
            else:
                raise ValueError(f"Tipo inválido: {request.tipo}")

            logger.info(f"✅ ETL concluído: {log_id}")
            return log_id
        finally:
            await orchestrator.extractor.close()

    background_tasks.add_task(run_etl_background_task, log.id)

    return ETLResponse(
        status="INICIADO",
        mensagem=f"ETL {request.tipo} iniciado para {request.ano}/{request.uf or 'TODAS'}",
        log_id=str(log.id),
        detalhes={
            "ano": request.ano,
            "uf": request.uf,
            "tipo": request.tipo,
        }
    )

