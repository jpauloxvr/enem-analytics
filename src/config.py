from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "microdados_enem_2025"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
IMAGES_DIR = PROJECT_ROOT / "images"

AREAS = ["CN", "CH", "LC", "MT"]

BLANK_SHEET_CODE = 3

RESULT_COLUMNS = [
    "SG_UF_ESC", "SG_UF_PROVA", "TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC",
    "TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT",
    "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT",
    "TP_STATUS_REDACAO", "NU_NOTA_REDACAO",
]

UF_REGION = {
    "AC": "Norte", "AM": "Norte", "AP": "Norte", "PA": "Norte",
    "RO": "Norte", "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste",
    "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MS": "Centro-Oeste",
    "MT": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}

SCHOOL_TYPE_NAMES = {1: "Federal", 2: "Estadual", 3: "Municipal", 4: "Privada"}

NETWORK_NAMES = {1: "Public", 2: "Public", 3: "Public", 4: "Private"}
