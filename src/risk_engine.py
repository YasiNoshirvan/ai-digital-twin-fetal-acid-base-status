import numpy as np
import pandas as pd


def assign_risk_band(probability):
    """
    Assign risk band based on probability.
    """
    if probability < 0.05:
        return "Low"
    if probability <= 0.20:
        return "Moderate"
    return "High"


def monte_carlo_acid_base_risk(
    ph_mean,
    ph_std,
    bd_mean,
    bd_std,
    n_samples=10000,
    random_state=42,
):
    """
    Estimate acidemia and metabolic acidosis risk using Monte Carlo sampling.
    """
    rng = np.random.default_rng(random_state)

    ph_samples = rng.normal(ph_mean, ph_std, size=n_samples)
    bd_samples = rng.normal(bd_mean, bd_std, size=n_samples)

    risks = {
        "P_pH_lt_720": float((ph_samples < 7.20).mean()),
        "P_pH_lt_710": float((ph_samples < 7.10).mean()),
        "P_pH_lt_700": float((ph_samples < 7.00).mean()),
        "P_met_acidosis_12": float(((ph_samples < 7.00) & (bd_samples >= 12)).mean()),
        "P_met_acidosis_16": float(((ph_samples < 7.00) & (bd_samples >= 16)).mean()),
    }

    risks["risk_band_pH_lt_720"] = assign_risk_band(risks["P_pH_lt_720"])
    risks["risk_band_met_acidosis_12"] = assign_risk_band(risks["P_met_acidosis_12"])

    return risks


def risk_stratification_summary(risk_df, band_column):
    """
    Count patients in each risk band.
    """
    return (
        risk_df[band_column]
        .value_counts()
        .rename_axis("risk_band")
        .reset_index(name="n_patients")
    )
