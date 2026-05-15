import re
from pathlib import Path

import pandas as pd


def parse_gestational_age(value):
    """
    Convert gestational age values such as '37W' or numeric weeks to float.
    """
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip().upper()
    match = re.search(r"(\d+(\.\d+)?)", value)

    if match:
        return float(match.group(1))

    return None


def load_case_file(file_path, group_label):
    """
    Load one case file and add group_doppler label.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    elif file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    df = standardize_columns(df)
    df["group_doppler"] = int(group_label)

    return df


def standardize_columns(df):
    """
    Standardize common column names to English-friendly labels.

    This function may need minor adaptation depending on local column names.
    """
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    rename_map = {
        "GA": "Gestational_Age",
        "Gestational Age": "Gestational_Age",
        "gestational age": "Gestational_Age",
        "Maternal Age": "Maternal_Age",
        "maternal age": "Maternal_Age",
        "Age": "Maternal_Age",
        "UA/PI": "UA_PI",
        "UA PI": "UA_PI",
        "UA_PI": "UA_PI",
        "PH": "pH",
        "ph": "pH",
        "PCO2": "pCO2",
        "pCO2": "pCO2",
        "BE": "BE",
        "Base Excess": "BE",
    }

    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns})

    if "Gestational_Age" in df.columns:
        df["Gestational_Age"] = df["Gestational_Age"].apply(parse_gestational_age)

    numeric_cols = ["Gestational_Age", "Maternal_Age", "UA_PI", "pH", "pCO2", "BE"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def load_and_merge_cases(normal_path, abnormal_path):
    """
    Load normal and abnormal Doppler case files and merge them into one dataset.
    """
    normal_df = load_case_file(normal_path, group_label=0)
    abnormal_df = load_case_file(abnormal_path, group_label=1)

    merged = pd.concat([normal_df, abnormal_df], ignore_index=True)

    required = ["Gestational_Age", "Maternal_Age", "UA_PI", "pH", "pCO2", "BE", "group_doppler"]
    missing = [col for col in required if col not in merged.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return merged[required].copy()
