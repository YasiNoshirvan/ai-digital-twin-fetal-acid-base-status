import pandas as pd


PLAUSIBILITY_RANGES = {
    "Gestational_Age": (20, 45),
    "Maternal_Age": (12, 55),
    "pH": (6.80, 7.60),
    "pCO2": (10, 90),
    "BE": (-30, 20),
    "UA_PI": (0.2, 3.0),
}


def add_qc_flags(df, ranges=None):
    """
    Add plausibility flags for each clinical variable.
    """
    df = df.copy()
    ranges = ranges or PLAUSIBILITY_RANGES

    for col, (lower, upper) in ranges.items():
        flag_col = f"flag_{col.lower()}_outlier"
        df[flag_col] = df[col].isna() | (df[col] < lower) | (df[col] > upper)

    flag_cols = [c for c in df.columns if c.startswith("flag_")]
    df["any_qc_flag"] = df[flag_cols].any(axis=1)

    return df


def build_qc_error_table(df):
    """
    Build a long-format table listing flagged records and reasons.
    """
    flag_cols = [c for c in df.columns if c.startswith("flag_") and c.endswith("_outlier")]

    rows = []

    for idx, row in df.iterrows():
        for flag_col in flag_cols:
            if bool(row[flag_col]):
                variable = (
                    flag_col
                    .replace("flag_", "")
                    .replace("_outlier", "")
                )

                rows.append(
                    {
                        "row_index": idx,
                        "variable": variable,
                        "value": row.get(variable, None),
                        "issue": "outside_plausible_range_or_missing",
                    }
                )

    return pd.DataFrame(rows)


def clean_strict(df):
    """
    Strict cleaning: remove records with any QC flag.
    """
    return df.loc[~df["any_qc_flag"]].reset_index(drop=True)


def clean_soft(df):
    """
    Soft cleaning: remove records with implausible core acid-base values.
    """
    severe_flags = [
        "flag_ph_outlier",
        "flag_pco2_outlier",
    ]

    existing = [col for col in severe_flags if col in df.columns]

    if not existing:
        return df.copy().reset_index(drop=True)

    mask = ~df[existing].any(axis=1)

    return df.loc[mask].reset_index(drop=True)
