# AI Digital Twin of Fetal Acid-Base Status from Umbilical Artery Doppler 🧬🤖

This repository contains a public and sanitized machine learning pipeline for building an AI-based digital twin of fetal acid-base status using umbilical artery Doppler and maternal clinical features.

The project focuses on predicting postnatal umbilical artery blood gas indicators, estimating uncertainty, assessing the added predictive value of UA_PI, and supporting risk-aware timing-of-delivery decision support.

---

## 🌍 Overview

Fetal acid-base status is an important indicator of fetal wellbeing and can reflect hypoxia, acidemia, or metabolic acidosis. However, direct postnatal blood gas measurements are only available after delivery.

This project investigates whether prenatal non-invasive Doppler information, especially umbilical artery pulsatility index, together with basic maternal and gestational variables, can be used to estimate fetal acid-base status before delivery.

The pipeline is designed as a probabilistic and interpretable AI workflow that supports:

- Regression prediction of acid-base indicators
- Binary endpoint definition for acidemia and metabolic acidosis
- Uncertainty estimation using prediction intervals
- Risk stratification
- Causal assessment of the added value of UA_PI
- Decision-support analysis

---

## 🎯 Objectives

The main objectives of this project are:

- Predict fetal acid-base indicators from prenatal Doppler and clinical features.
- Estimate `pH`, `pCO2`, and `Base Excess`.
- Quantify uncertainty using prediction intervals.
- Estimate risk probabilities for acidemia and metabolic acidosis endpoints.
- Evaluate whether UA_PI adds predictive value beyond gestational age and maternal age.
- Compare baseline clinical models with Doppler-added and machine learning models.
- Build a decision-support framework using risk bands and uncertainty-aware predictions.
- Explore causal evidence for the independent association between abnormal UA_PI and acid-base outcomes.

---

## 🧪 Dataset

The original dataset contains two groups:

- Normal umbilical artery Doppler cases
- Abnormal umbilical artery Doppler cases

The main variables include:

| Variable | Description |
|---|---|
| `Gestational_Age` | Gestational age at examination or delivery |
| `Maternal_Age` | Maternal age |
| `UA_PI` | Umbilical artery pulsatility index |
| `pH` | Umbilical artery blood gas pH |
| `pCO2` | Partial pressure of carbon dioxide |
| `BE` | Base Excess |

Due to clinical data protection, research confidentiality, and manuscript submission status, the original dataset is **not included** in this repository.

Only generalized code, methodological documentation, and synthetic/demo examples are provided.

---

## 🛠️ Methodology

The workflow includes:

1. Data ingestion and harmonization
2. Data audit and plausibility checks
3. Strict and soft cleaning scenarios
4. Exploratory data analysis
5. Acid-base endpoint definition
6. Baseline and machine learning model evaluation
7. Added-value analysis of UA_PI
8. Prediction interval estimation
9. Risk engine for acidemia and metabolic acidosis
10. Causal analysis
11. Decision curve analysis
12. Robustness and sensitivity checks

---

## 🧹 Data Quality Control

The pipeline includes clinical plausibility rules to flag potentially invalid values:

| Variable | Plausible Range |
|---|---|
| `Gestational_Age` | 20–45 weeks |
| `Maternal_Age` | 12–55 years |
| `pH` | 6.80–7.60 |
| `pCO2` | 10–90 mmHg |
| `BE` | -30 to +20 |
| `UA_PI` | 0.2–3.0 |

The code supports two cleaning strategies:

- **Strict scenario:** remove records with any flagged outlier
- **Soft scenario:** remove only severe or outcome-specific implausible records

---

## 🧬 Endpoints

The project defines both continuous and binary outcomes.

### Continuous outcomes

- `pH`
- `pCO2`
- `BE`

### Binary acid-base endpoints

| Endpoint | Definition |
|---|---|
| `acidemia_720` | `pH < 7.20` |
| `acidemia_710` | `pH < 7.10` |
| `acidemia_700` | `pH < 7.00` |
| `met_acidosis_12` | `pH < 7.00` and `Base Deficit >= 12` |
| `met_acidosis_16` | `pH < 7.00` and `Base Deficit >= 16` |

Base Deficit is calculated as:

```text
BD = -BE
