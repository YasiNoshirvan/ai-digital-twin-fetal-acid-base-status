# Data Dictionary

| Variable | Description | Type |
|---|---|---|
| `Gestational_Age` | Gestational age in completed weeks | Numeric |
| `Maternal_Age` | Maternal age in years | Numeric |
| `UA_PI` | Umbilical artery pulsatility index | Numeric |
| `pH` | Umbilical artery blood gas pH | Numeric |
| `pCO2` | Partial pressure of carbon dioxide | Numeric |
| `BE` | Base Excess | Numeric |
| `group_doppler` | Doppler group label: 0 = normal, 1 = abnormal | Binary |
| `BD` | Base Deficit, calculated as `-BE` | Numeric |
| `acidemia_720` | Binary endpoint: `pH < 7.20` | Binary |
| `acidemia_710` | Binary endpoint: `pH < 7.10` | Binary |
| `acidemia_700` | Binary endpoint: `pH < 7.00` | Binary |
| `met_acidosis_12` | Binary endpoint: `pH < 7.00` and `BD >= 12` | Binary |
| `met_acidosis_16` | Binary endpoint: `pH < 7.00` and `BD >= 16` | Binary |
