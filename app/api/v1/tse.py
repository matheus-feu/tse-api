import uuid

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repository.log_repository import ETLLogRepository
from app.schemas.etl_schema import ETLResponse, ETLRequest
from app.services.etl.etl_orchestrator import ETLOrchestrator

router = APIRouter()


@router.get("/etl/logs/{log_id}")
async def get_status_job(log_id: str, db: AsyncSession = Depends(get_db_session)):
    """
    Consulta o status do job ETL pelo log_id retornado ao iniciar o processo ETL.
    """
    repo = ETLLogRepository(db)
    log = await repo.find_by_id(log_id)

    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job/log '{log_id}' não encontrado")
    return {
        "id": str(log.id),
        "process_name": log.process_name,
        "status": log.status,
        "start_time": log.start_time.isoformat() if log.start_time else None,
        "end_time": log.end_time.isoformat() if log.end_time else None,
        "records_processed": log.records_processed,
        "error_message": log.error_message
    }


@router.post("/etl/execute", response_model=ETLResponse)
async def execute_etl(
        request: ETLRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db_session)
):
    """
    Inicia o processo ETL para dados do TSE em segundo plano.
    """
    job_uuid = str(uuid.uuid4())

    try:
        logger.info(f"🚀 Iniciando ETL: {request.tipo} - {request.ano}/{request.uf}")
        orchestrator = ETLOrchestrator(db_session=db)

        if request.tipo == "candidato":
            background_tasks.add_task(
                orchestrator.run_etl_votation_candidate,
                ano=request.ano,
                uf=request.uf,
            )
        elif request.tipo == "partido":
            background_tasks.add_task(
                orchestrator.run_etl_votacao_partido,
                ano=request.ano,
                uf=request.uf,
            )
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tipo inválido. Use: 'candidato', 'partido' ou 'completo'")

        logger.info(f"✅ ETL iniciado em background: {job_uuid}")

        return ETLResponse(
            status="INICIADO",
            mensagem=f"ETL {request.tipo} iniciado para {request.ano}/{request.uf or 'TODAS'}",
            log_id=job_uuid,
            detalhes={
                "ano": request.ano,
                "uf": request.uf,
                "tipo": request.tipo,
            }
        )
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar ETL: {e}", exc_info=True)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Erro ao iniciar ETL: {str(e)}")
