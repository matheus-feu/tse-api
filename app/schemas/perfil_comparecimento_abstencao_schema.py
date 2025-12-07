from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PerfilComparecimentoAbstencaoResponse(BaseModel):
    id: UUID

    dt_geracao: str | None = None
    hh_geracao: str | None = None
    ano_eleicao: int | None = None
    nr_turno: int | None = None
    sg_uf: str | None = None
    cd_municipio: int | None = None
    nm_municipio: str | None = None
    nr_zona: int | None = None
    cd_genero: int | None = None
    ds_genero: str | None = None
    cd_estado_civil: int | None = None
    ds_estado_civil: str | None = None
    cd_faixa_etaria: int | None = None
    ds_faixa_etaria: str | None = None
    cd_grau_escolaridade: int | None = None
    ds_grau_escolaridade: str | None = None
    cd_cor_raca: int | None = None
    ds_cor_raca: str | None = None
    cd_quilombola: int | None = None
    ds_quilombola: str | None = None
    cd_interprete_libras: int | None = None
    ds_interprete_libras: str | None = None
    cd_identidade_genero: int | None = None
    ds_identidade_genero: str | None = None
    cd_idioma_indigena: int | None = None
    ds_idioma_indigena: str | None = None
    cd_grupo_indigena: int | None = None
    ds_grupo_indigena: str | None = None
    qt_aptos: int | None = None
    qt_comparecimento: int | None = None
    qt_abstencao: int | None = None
    qt_comparecimento_deficiencia: int | None = None
    qt_abstencao_deficiencia: int | None = None
    qt_comparecimento_tte: int | None = None
    qt_abstencao_tte: int | None = None
    qt_comparec_facultativo: int | None = None
    qt_abst_facultativo: int | None = None
    qt_comparec_obrigatorio: int | None = None
    qt_abst_obrigatorio: int | None = None
    qt_comparec_defic_facultativo: int | None = None
    qt_abst_defic_facultativo: int | None = None
    qt_comparec_defic_obrigatorio: int | None = None
    qt_abst_defic_obrigatorio: int | None = None

    model_config = ConfigDict(from_attributes=True)
