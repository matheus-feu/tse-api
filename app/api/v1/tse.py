from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.etl_schema import ETLResponse, ETLRequest
from app.services.etl.etl_orchestrator import ETLOrchestrator

router = APIRouter()


@router.post("/etl/execute", response_model=ETLResponse)
async def execute_etl(
        request: ETLRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db_session)
):
    """
    Inicia o processo ETL para dados do TSE em segundo plano.
    """
    try:
        logger.info(f"🚀 Iniciando ETL: {request.tipo} - {request.ano}/{request.uf}")

        orchestrator = ETLOrchestrator(db_session=db)

        job_id = f"etl_{request.tipo}_{request.ano}_{request.uf or 'BR'}_{int(datetime.utcnow().timestamp())}"

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
            raise HTTPException(400, "Tipo inválido. Use: 'candidato', 'partido' ou 'completo'")

        logger.info(f"✅ ETL iniciado em background: {job_id}")

        return ETLResponse(
            status="INICIADO",
            mensagem=f"ETL {request.tipo} iniciado para {request.ano}/{request.uf or 'TODAS'}",
            log_id=job_id,
            detalhes={
                "ano": request.ano,
                "uf": request.uf,
                "tipo": request.tipo,
            }
        )
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar ETL: {e}", exc_info=True)
        raise HTTPException(500, f"Erro ao iniciar ETL: {str(e)}")
