import pandas as pd

from .config import (
    AREAS, BLANK_SHEET_CODE, NETWORK_NAMES, PROCESSED_DIR, RAW_DIR,
    RESULT_COLUMNS, SCHOOL_TYPE_NAMES, UF_REGION,
)

CACHE_PATH = PROCESSED_DIR / "results_2025_selected_columns.parquet"


def results_csv_path(raw_dir=RAW_DIR):
    return raw_dir / "DADOS" / "RESULTADOS_2025.csv"


def load_results(use_cache=True):
    if use_cache and CACHE_PATH.exists():
        return pd.read_parquet(CACHE_PATH)
    df = pd.read_csv(
        results_csv_path(), sep=";", encoding="latin-1", usecols=RESULT_COLUMNS
    )
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CACHE_PATH)
    return df


def recode_blank_sheets(df):
    df = df.copy()
    for area in AREAS:
        presence = f"TP_PRESENCA_{area}"
        score = f"NU_NOTA_{area}"
        original = presence + "_ORIG"
        if original not in df.columns:
            df[original] = df[presence]
        blank = (df[original] == 1) & ((df[score] == 0) | df[score].isna())
        df.loc[blank, presence] = BLANK_SHEET_CODE
        df.loc[blank, score] = float("nan")
    return df


def add_region(df, state_column="SG_UF_PROVA", new_column="REGION"):
    df = df.copy()
    df[new_column] = df[state_column].map(UF_REGION)
    return df


def build_school_subset(df):
    subset = df[df["TP_DEPENDENCIA_ADM_ESC"].notna()].copy()
    subset["SCHOOL_TYPE"] = subset["TP_DEPENDENCIA_ADM_ESC"].map(SCHOOL_TYPE_NAMES)
    subset["NETWORK"] = subset["TP_DEPENDENCIA_ADM_ESC"].map(NETWORK_NAMES)
    subset["SCHOOL_REGION"] = subset["SG_UF_ESC"].map(UF_REGION)
    return subset


def prepare_dataset(use_cache=True):
    df = load_results(use_cache=use_cache)
    df = recode_blank_sheets(df)
    df = add_region(df)
    return df, build_school_subset(df)
