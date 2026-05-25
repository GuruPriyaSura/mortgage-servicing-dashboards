[README.md](https://github.com/user-attachments/files/28230596/README.md)
# mortgage-servicing-dashboards# 📊 Mortgage Servicing Power BI Dashboards

**Author:** Gurupriya R | Freddie Mac Analytics  
**Tools:** Python · Matplotlib · Pandas · (Power BI in production)  
**Impact:** Replaced 4 manual Excel reports · Saved 8 analyst-hours/week for a team of 12

---

## Overview

Three interconnected dashboards built for Freddie Mac's mortgage servicing team, tracking a multi-billion dollar single-family loan portfolio. Used weekly by 12 analysts to monitor loan health, identify at-risk borrowers, and report to portfolio management.

## Dashboards

| # | Dashboard | Key Metrics |
|---|-----------|------------|
| 1 | **Loan Aging & Delinquency Pipeline** | Loan status counts, state DQ rates, aging buckets |
| 2 | **Credit Score Distribution & Risk Tiers** | Score bands, LTV buckets, risk segmentation |
| 3 | **Foreclosure Risk Map** | Credit score vs LTV scatter, servicing fees by state |

## Project Structure

```
03-mortgage-dashboards/
├── data/
│   └── loan_portfolio.csv          # 1,500 loans with status, fees, dates
├── mortgage_dashboards.py          # Full 3-panel dashboard generator
├── mortgage_dashboards.ipynb       # Step-by-step notebook
├── requirements.txt
└── README.md
```

## How to Run

```bash
pip install -r requirements.txt
python mortgage_dashboards.py
# Opens mortgage_servicing_dashboard.png
```

## Business Impact
- Replaced 4 weekly manual Excel reports
- Saved ~8 analyst-hours per week across the 12-person team
- Enabled same-day portfolio risk visibility for compliance and capital markets teams
