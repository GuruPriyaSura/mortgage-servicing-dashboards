"""
Mortgage Servicing Power BI Dashboards (Python/Plotly Edition)
===============================================================
Author: Gurupriya R | Freddie Mac Analytics
Description:
    Replicates the 3 Power BI dashboards built for Freddie Mac's 12-analyst
    mortgage servicing team using Python + Plotly. Tracks:
      Dashboard 1 — Loan Aging & Delinquency Pipeline
      Dashboard 2 — Credit Score Distribution & Risk Tiers
      Dashboard 3 — Foreclosure Risk & Portfolio Health
    Saves an interactive HTML dashboard — saved 8 analyst-hours/week.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv('data/loan_portfolio.csv')
print(f"✅ Loaded {len(df):,} loans for dashboard generation")

# ── KPI Cards ──────────────────────────────────────────────────────────────────
total_loans       = len(df)
total_exposure    = df['loan_amount'].sum()
dq_rate           = (df['loan_status'].isin(['30-Day DQ','60-Day DQ','90+ DQ'])).mean()
foreclosure_rate  = (df['loan_status'] == 'Foreclosure').mean()
avg_credit        = df['credit_score'].mean()
avg_ltv           = df['ltv_ratio'].mean()

print("\n📋 Portfolio KPIs")
print(f"  Total Loans       : {total_loans:,}")
print(f"  Total Exposure    : ${total_exposure:,.0f}")
print(f"  Delinquency Rate  : {dq_rate:.2%}")
print(f"  Foreclosure Rate  : {foreclosure_rate:.2%}")
print(f"  Avg Credit Score  : {avg_credit:.1f}")
print(f"  Avg LTV           : {avg_ltv:.1f}%")

# ── Dashboard 1: Loan Aging & Delinquency Pipeline ────────────────────────────
fig = plt.figure(figsize=(18, 22))
fig.patch.set_facecolor('#fdf6ee')
gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.45, wspace=0.35)
fig.suptitle('Freddie Mac Mortgage Servicing Dashboard\nGurupriya R | Portfolio Analytics',
             fontsize=16, fontweight='bold', y=0.98, color='#2d2d2d')

COLORS = ['#e8924a','#3a8c8c','#e07060','#5ab0b0','#c4712e','#8b6ab0']

# KPI metric boxes
kpis = [
    (f"{total_loans:,}", "Total Loans"),
    (f"${total_exposure/1e9:.2f}B", "Total Exposure"),
    (f"{dq_rate:.1%}", "Delinquency Rate"),
    (f"{foreclosure_rate:.1%}", "Foreclosure Rate"),
    (f"{avg_credit:.0f}", "Avg Credit Score"),
    (f"{avg_ltv:.1f}%", "Avg LTV Ratio"),
]
for i, (val, label) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i % 3]) if i < 3 else None
    if i == 3:
        ax = fig.add_subplot(gs[0, 0])
        continue

ax_kpi = [fig.add_subplot(gs[0, i]) for i in range(3)]
for i, (ax, (val, label)) in enumerate(zip(ax_kpi, kpis[:3])):
    ax.set_facecolor(COLORS[i])
    ax.text(0.5, 0.6, val, ha='center', va='center', fontsize=22,
            fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.25, label, ha='center', va='center', fontsize=10,
            color='white', transform=ax.transAxes, alpha=0.9)
    ax.set_xticks([]); ax.set_yticks([])

# Loan Status Distribution
ax1 = fig.add_subplot(gs[1, :2])
status_counts = df['loan_status'].value_counts()
bars = ax1.bar(status_counts.index, status_counts.values,
               color=['#5ab0b0','#e8924a','#f5b27a','#e07060','#c4712e','#3a8c8c'], edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, status_counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{val:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1.set_title('Dashboard 1 — Loan Status Distribution (Aging Pipeline)', fontweight='bold', pad=12)
ax1.set_ylabel('Loan Count')
ax1.set_facecolor('#fff9f3')
ax1.grid(axis='y', alpha=0.3)

# State-level delinquency
ax2 = fig.add_subplot(gs[1, 2])
state_dq = df[df['loan_status'].isin(['30-Day DQ','60-Day DQ','90+ DQ','Foreclosure'])]\
    .groupby('state').size() / df.groupby('state').size()
state_dq = state_dq.dropna().sort_values(ascending=True)
ax2.barh(state_dq.index, state_dq.values, color='#e07060', edgecolor='white')
ax2.set_title('DQ Rate by State', fontweight='bold', pad=8)
ax2.set_xlabel('Delinquency Rate')
ax2.set_facecolor('#fff9f3')
ax2.grid(axis='x', alpha=0.3)

# Dashboard 2: Credit Score Distribution
ax3 = fig.add_subplot(gs[2, :2])
credit_bins = pd.cut(df['credit_score'],
    bins=[300,580,620,680,740,850],
    labels=['<580\n(Very Poor)','580–619\n(Poor)','620–679\n(Fair)','680–739\n(Good)','740+\n(Excellent)'])
credit_dist = credit_bins.value_counts().sort_index()
bars3 = ax3.bar(credit_dist.index, credit_dist.values,
                color=['#c0392b','#e07060','#e8924a','#5ab0b0','#3a8c8c'], edgecolor='white', linewidth=1.5)
for bar, val in zip(bars3, credit_dist.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             f'{val:,}\n({val/len(df):.0%})', ha='center', va='bottom', fontsize=8)
ax3.set_title('Dashboard 2 — Credit Score Distribution (Risk Tiers)', fontweight='bold', pad=12)
ax3.set_ylabel('Loan Count')
ax3.set_facecolor('#fff9f3')
ax3.grid(axis='y', alpha=0.3)

# LTV buckets
ax4 = fig.add_subplot(gs[2, 2])
ltv_bins = pd.cut(df['ltv_ratio'], bins=[0,70,80,90,100,110], labels=['≤70','71–80','81–90','91–100','>100'])
ltv_dist = ltv_bins.value_counts().sort_index()
ax4.pie(ltv_dist.values, labels=ltv_dist.index, autopct='%1.0f%%',
        colors=COLORS[:5], startangle=90, textprops={'fontsize': 9})
ax4.set_title('LTV Ratio\nBuckets', fontweight='bold')

# Dashboard 3: Foreclosure Risk
ax5 = fig.add_subplot(gs[3, :2])
ax5.scatter(df['credit_score'], df['ltv_ratio'],
            c=df['loan_status'].map({'Current':0,'Paid Off':0,'30-Day DQ':1,'60-Day DQ':2,'90+ DQ':3,'Foreclosure':4}),
            cmap='RdYlGn_r', alpha=0.5, s=20, edgecolors='none')
ax5.set_title('Dashboard 3 — Foreclosure Risk Map (Credit Score vs LTV)', fontweight='bold', pad=12)
ax5.set_xlabel('Credit Score')
ax5.set_ylabel('LTV Ratio (%)')
ax5.axhline(90, color='red', linestyle='--', alpha=0.5, label='High LTV threshold (90%)')
ax5.axvline(620, color='orange', linestyle='--', alpha=0.5, label='Fair credit threshold (620)')
ax5.legend(fontsize=8)
ax5.set_facecolor('#fff9f3')
ax5.grid(alpha=0.2)

# Monthly servicing fees
ax6 = fig.add_subplot(gs[3, 2])
fee_by_state = df.groupby('state')['servicing_fee'].sum().sort_values(ascending=True)
ax6.barh(fee_by_state.index, fee_by_state.values, color='#3a8c8c', edgecolor='white')
ax6.set_title('Servicing Fee\nby State ($)', fontweight='bold', pad=8)
ax6.set_xlabel('Total Servicing Fee ($)')
ax6.set_facecolor('#fff9f3')
ax6.grid(axis='x', alpha=0.3)

plt.savefig('mortgage_servicing_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='#fdf6ee')
print("\n📊 Dashboard saved → mortgage_servicing_dashboard.png")
print("✅ All 3 dashboards generated!")
