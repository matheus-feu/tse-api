PROCESS_CONFIG = {
    "candidato": {
        "func": "run_etl_votation_candidate",
        "extra_args": {
            "process_type": "votacao_candidato_munzona"
        }
    },
    "partido": {
        "func": "run_etl_votation_partido",
        "extra_args": {
            "process_type": "votacao_partido_munzona"
        }
    },
}
