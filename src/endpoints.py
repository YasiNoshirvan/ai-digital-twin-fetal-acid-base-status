import numpy as np
import pandas as pd


def add_base_deficit(df, be_col="BE"):
    """
    Add Base Deficit as the negative of Base Excess.
    """
    df = df.copy()
    df["BD"] = -df[be_col]
    return df


def add_acid_base_endpoints(df):
    """
    Add binary acidemia and metabolic acidosis endpoints.
    """
    df = add_base_deficit(df)

    df["acidemia_720"] = (df["pH"] < 7.20).astype(int)
    df["acidemia_710"] = (df["pH"] < 7.10).astype(int)
    df["acidemia_700"] = (df["pH"] < 7.00).astype(int)

    df["met_acidosis_12"] = ((df["pH"] < 7.00) & (df["BD"] >= 12)).astype(int)
    df["met_acidosis_16"] = ((df["pH"] < 7.00) & (df["BD"] >= 16)).astype(int)

    return df


def endpoint_prevalence(df, group_col="group_doppler"):
    """
    Build endpoint prevalence table overall and by Doppler group.
    """
    endpoints = [
        "acidemia_720",
        "acidemia_710",
        "acidemia_700",
        "met_acidosis_12",
        "met_acidosis_16",
    ]

    rows = []

    for endpoint in endpoints:
        rows.append(
            {
                "endpoint_name": endpoint,
                "group": "overall",
                "n_total": len(df),
                "n_pos": int(df[endpoint].sum()),
                "prevalence": float(df[endpoint].mean()),
            }
        )

        for group_value, group_df in df.groupby(group_col):
            rows.append(
                {
                    "endpoint_name": endpoint,
                    "group": group_value,
                    "n_total": len(group_df),
                    "n_pos": int(group_df[endpoint].sum()),
                    "prevalence": float(group_df[endpoint].mean()),
                }
            )

    return pd.DataFrame(rows)


def endpoint_feasibility(df):
    """
    Assess whether each endpoint is feasible for binary modelling.
    """
    endpoints = [
        "acidemia_720",
        "acidemia_710",
        "acidemia_700",
        "met_acidosis_12",
        "met_acidosis_16",
    ]

    rows = []

    for endpoint in endpoints:
        n_pos = int(df[endpoint].sum())
        n_neg = int(len(df) - n_pos)

        if n_pos < 10:
            status = "Descriptive only"
            plan = "Deferred to Phase B; needs more positive cases"
        elif n_pos < 30:
            status = "Low-prevalence endpoint"
            plan = "Model with caution; prioritize AUPRC and confidence intervals"
        else:
            status = "Suitable for binary modelling"
            plan = "Can be considered for primary binary modelling"

        rows.append(
            {
                "endpoint_name": endpoint,
                "n_pos": n_pos,
                "n_neg": n_neg,
                "feasibility_status": status,
                "modeling_plan": plan,
            }
        )

    return pd.DataFrame(rows)
