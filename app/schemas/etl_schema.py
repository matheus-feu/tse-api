from enum import Enum
from typing import Optional
from wsgiref.validate import validator

from pydantic import BaseModel, Field


class UFEnum(str, Enum):
    """Unidades Federativas do Brasil."""
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


class TipoETLEnum(str, Enum):
    """Tipos de ETL disponíveis."""
    CANDIDATO = "candidato"
    PARTIDO = "partido"



class ETLRequest(BaseModel):
    """Request para iniciar ETL."""
    ano: int = Field(..., ge=2000, le=2030, description="Ano da eleição")
    uf: Optional[UFEnum] = Field(None, description="UF brasileira (ex: SP, RJ)")
    tipo: TipoETLEnum = Field(
        TipoETLEnum.CANDIDATO,
        description="Tipo de ETL: candidato ou partido"
    )


class ETLResponse(BaseModel):
    """Response de ETL."""
    status: str
    mensagem: str
    log_id: str
    detalhes: Optional[dict] = None
