# Methodology

This document describes the public and sanitized methodology of the project.

The original study was developed as part of a submitted medical AI manuscript. The repository does not include real clinical datasets, restricted internal documents, or patient-level outputs.

---

## 1. Project Aim

The aim of this project is to develop a probabilistic AI pipeline for estimating fetal acid-base status using non-invasive prenatal Doppler and maternal clinical features.

The target outcomes include:

- Umbilical artery blood gas `pH`
- `pCO2`
- Base Excess `BE`
- Derived acidemia and metabolic acidosis endpoints

The broader goal is to support uncertainty-aware fetal risk assessment and timing-of-delivery decision-support research.

---

## 2. Data Sources

The original study uses two clinical groups:

- Normal umbilical artery Doppler cases
- Abnormal umbilical artery Doppler cases

The expected core variables are:

| Variable | Description |
|---|---|
| `Gestational_Age` | Gestational age in weeks |
| `Maternal_Age` | Maternal age in years |
| `UA_PI` | Umbilical artery pulsatility index |
| `pH` | Umbilical artery blood gas pH |
| `pCO2` | Partial pressure of carbon dioxide |
| `BE` | Base Excess |
| `group_doppler` | Doppler group: 0 = normal, 1 = abnormal |

The original clinical data are not included in this public repository.

---

## 3. Data Ingestion and Harmonization

The first step of the pipeline loads the normal and abnormal case files and harmonizes them into one unified dataset.

Main operations include:

- Reading tabular files from CSV or Excel format
- Standardizing column names
- Parsing gestational age values
- Converting variables to numeric format
- Creating a binary Doppler group label:
  - `0 = normal Doppler`
  - `1 = abnormal Doppler`

Gestational age values may appear as either numeric values or text formats such as `37W`. These values are converted into numeric week values.

---

## 4. Data Quality Control

Clinical plausibility checks are applied to identify potentially invalid or suspicious values.

The default plausibility ranges are:

| Variable | Plausible Range |
|---|---|
| `Gestational_Age` | 20–45 weeks |
| `Maternal_Age` | 12–55 years |
| `pH` | 6.80–7.60 |
| `pCO2` | 10–90 mmHg |
| `BE` | -30 to +20 |
| `UA_PI` | 0.2–3.0 |

For each variable, the pipeline creates outlier flags such as:

- `flag_ph_outlier`
- `flag_pco2_outlier`
- `flag_be_outlier`
- `flag_ua_pi_outlier`

A long-format quality-control error table can also be generated to document which rows were flagged and why.

---

## 5. Cleaning Scenarios

Two cleaning strategies are supported.

### Scenario A: Strict Cleaning

The strict scenario removes records with any quality-control flag.

This scenario is useful for sensitivity analysis and for evaluating the model under conservative data-cleaning assumptions.

### Scenario B: Soft Cleaning

The soft scenario removes only records with severe or outcome-specific implausible values, such as clearly invalid `pH` or `pCO2`.

This scenario preserves more data while still reducing the influence of extreme data-entry errors.

---

## 6. Exploratory Data Analysis

The exploratory analysis compares normal and abnormal Doppler groups.

The main variables analyzed are:

- Gestational age
- Maternal age
- UA_PI
- pH
- pCO2
- BE

Recommended descriptive summaries include:

- Mean and standard deviation
- Median and interquartile range
- Missing-value counts
- Group-wise comparisons

Recommended visualizations include:

- Boxplots or violin plots for acid-base outcomes by Doppler group
- Scatter plots of `UA_PI` versus `pH`
- Scatter plots of `UA_PI` versus `BE`
- Scatter plots of gestational age versus `UA_PI`

---

## 7. Endpoint Definition

The project includes continuous outcomes and binary acid-base endpoints.

### Continuous Outcomes

| Outcome | Description |
|---|---|
| `pH` | Umbilical artery blood gas pH |
| `pCO2` | Partial pressure of carbon dioxide |
| `BE` | Base Excess |

### Derived Variable

Base Deficit is calculated as:

```text
BD = -BE
