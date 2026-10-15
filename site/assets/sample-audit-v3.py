#!/usr/bin/env python3
"""Render the spaced v3 Harbor Stitch Apparel audit dashboard.

The constants are the captured results of the previously executed 2025
read-only SQL. This script performs no source access.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch


OUT = Path(__file__).resolve().parent
PNG = OUT / "harbor-audit-v3.png"
PDF = OUT / "harbor-audit-v3.pdf"

WHITE = "#FFFFFF"
GRAPHITE = "#263238"
MUTED = "#68777A"
TEAL = "#008B8B"
TEAL_DARK = "#006B6B"
AMBER = "#E69F00"
AMBER_LIGHT = "#FFF2D5"
GRID = "#DDE5E5"
PANEL = "#F7FAFA"

# Captured query 1: monthly production and orders.
months = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ordered = np.array([10699, 9254, 9868, 10228, 10903, 10292, 9558, 11100, 12002, 12636, 13218, 10770])
produced = ordered.copy()
good = np.array([10432, 9023, 9621, 9972, 10631, 10035, 9215, 10822, 11701, 12319, 12888, 10500])
defective = np.array([267, 231, 247, 256, 272, 257, 343, 278, 301, 317, 330, 270])
monthly_defect_rate = np.array([2.50, 2.50, 2.50, 2.50, 2.49, 2.50, 3.59, 2.50, 2.51, 2.51, 2.50, 2.51])

# Captured queries 2 and 8: annual and July defects by line.
line_names = np.array(["Line 2", "Line 3", "Line 1"])
line_units = np.array([43420, 43773, 43335])
line_defects = np.array([1188, 1097, 1084])
line_rates = np.array([2.74, 2.51, 2.50])
overall_defect_rate = 2.58
july_line_rates = {"Line 2": 5.83, "Line 1": 2.51, "Line 3": 2.51}

# Captured queries 3–6: payment tests and repeated-reference indicator.
duplicate_supplier = "Coastal Textile Mills"
duplicate_rows = [
    {"invoice_id": "AP-2025-07-V01", "reference": "V01-2025-007", "invoice_date": "2025-07-12",
     "amount": 3595.00, "payment_id": "P-AP-2025-07-V01", "payment_date": "2025-08-06"},
    {"invoice_id": "AP-2025-07-V01-COPY", "reference": "V01-2025-007", "invoice_date": "2025-07-12",
     "amount": 3595.00, "payment_id": "P-AP-2025-07-V01-COPY", "payment_date": "2025-08-07"},
]
multi_payment_invoice_count = 0
overpaid_invoice_count = 0

# Captured query 7: fabric efficiency by style.
style_names = np.array(["Workwear polo", "Crew-neck tee", "Cotton jogger", "Canvas jacket"])
product_ids = np.array(["T02", "T01", "T04", "T03"])
style_units = np.array([31387, 28004, 36977, 34160])
actual_fabric = np.array([39313.7, 27493.1, 63051.5, 80951.4])
standard_fabric = np.array([37664.4, 26603.8, 61012.1, 78568.0])
excess_fabric = np.array([1649.3, 889.3, 2039.4, 2383.4])
fabric_efficiency = np.array([95.8, 96.8, 96.8, 97.1])


def style_plot(ax, xgrid=False, ygrid=False):
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=11, length=0, pad=7)
    if xgrid:
        ax.grid(axis="x", color=GRID, linewidth=0.9, zorder=0)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.9, zorder=0)


def panel_header(fig, cell, number, title, subtitle, key=None):
    ax = fig.add_subplot(cell)
    ax.axis("off")
    ax.text(0.00, 0.82, f"{number}  {title}", fontsize=18, fontweight="bold",
            color=GRAPHITE, va="center")
    ax.text(0.00, 0.45, subtitle, fontsize=11, color=MUTED, va="center")
    if key:
        key_color, key_style, key_text = key
        ax.add_line(Line2D([0.0, 0.05], [0.06, 0.06], transform=ax.transAxes,
                           color=key_color, linewidth=2.0, linestyle=key_style))
        ax.text(0.065, 0.06, key_text, fontsize=10.5, color=GRAPHITE,
                va="center", ha="left")
    return ax


def add_kpi(fig, x, label, value, note, accent=TEAL):
    ax = fig.add_axes([x, 0.814, 0.205, 0.078])
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.012,rounding_size=0.025",
                                facecolor=PANEL, edgecolor=GRID, linewidth=1.0))
    ax.add_patch(FancyBboxPatch((0.025, 0.17), 0.013, 0.66, boxstyle="round,pad=0,rounding_size=0.006",
                                facecolor=accent, edgecolor=accent))
    ax.text(0.075, 0.73, label.upper(), color=MUTED, fontsize=9.5, fontweight="bold", va="center")
    ax.text(0.075, 0.43, value, color=GRAPHITE, fontsize=22, fontweight="bold", va="center")
    ax.text(0.075, 0.14, note, color=MUTED, fontsize=9.2, va="center")


def make_dashboard():
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": GRAPHITE})
    fig = plt.figure(figsize=(22, 16), dpi=180, facecolor=WHITE)

    fig.text(0.05, 0.956, "HARBOR STITCH APPAREL", fontsize=12, color=TEAL_DARK, fontweight="bold")
    fig.text(0.05, 0.922, "2025 operational audit dashboard", fontsize=29,
             color=GRAPHITE, fontweight="bold")
    fig.text(0.05, 0.893,
             "Preliminary screening • Production, quality, supplier payments and fabric usage • PostgreSQL records",
             fontsize=12, color=MUTED)
    fig.text(0.95, 0.948, "REVIEW INDICATORS", ha="right", color=AMBER,
             fontsize=11, fontweight="bold")
    fig.text(0.95, 0.920, "Fictional records • Not a certified audit opinion",
             ha="right", color=MUTED, fontsize=10.5)

    annual_units = int(produced.sum())
    total_defects = int(defective.sum())
    weighted_eff = 100 * standard_fabric.sum() / actual_fabric.sum()
    add_kpi(fig, 0.05, "Production", f"{annual_units:,}", "units; recorded orders matched")
    add_kpi(fig, 0.272, "Defect rate", f"{100 * total_defects / annual_units:.2f}%",
            f"{total_defects:,} defective units")
    add_kpi(fig, 0.494, "Payment review", "$3,595", "one of two matching paid records", AMBER)
    add_kpi(fig, 0.716, "Fabric efficiency", f"{weighted_eff:.1f}%",
            f"{excess_fabric.sum():,.1f} m above standard", AMBER)

    outer = fig.add_gridspec(2, 2, left=0.05, right=0.95, bottom=0.075, top=0.765,
                             hspace=0.32, wspace=0.43)

    # Panel 1: title and subtitle occupy their own row; the plot reserves top space.
    p1 = outer[0, 0].subgridspec(2, 1, height_ratios=[0.24, 0.76], hspace=0.02)
    panel_header(fig, p1[0], "01", "Monthly production",
                 "Bars: units produced • Line: defect rate • Orders matched production")
    ax1 = fig.add_subplot(p1[1])
    style_plot(ax1, ygrid=True)
    x = np.arange(len(months))
    bars = ax1.bar(x, produced / 1000, width=0.64, color=TEAL, edgecolor="none", zorder=2)
    bars[6].set_color(AMBER)
    ax1.set_xticks(x, months)
    ax1.set_ylabel("Produced units (thousands)", color=MUTED, fontsize=11, labelpad=10)
    ax1.set_ylim(0, 16.1)
    ax1.set_yticks([0, 5, 10, 15])
    ax1b = ax1.twinx()
    ax1b.set_ylim(2.20, 4.30)
    ax1b.plot(x, monthly_defect_rate, color=GRAPHITE, marker="o", markersize=5,
              linewidth=1.8, zorder=3)
    ax1b.scatter([6], [monthly_defect_rate[6]], s=90, color=AMBER,
                 edgecolor=WHITE, linewidth=1.4, zorder=4)
    ax1b.set_ylabel("Defect rate", color=MUTED, fontsize=11, labelpad=8)
    ax1b.set_yticks([2.5, 3.0, 3.5, 4.0], ["2.5%", "3.0%", "3.5%", "4.0%"])
    ax1b.tick_params(colors=MUTED, labelsize=11, length=0, pad=7)
    for spine in ax1b.spines.values():
        spine.set_visible(False)
    ax1b.annotate("JULY EXCEPTION\n3.59% • 343 defects", xy=(6, 3.59), xytext=(4.05, 4.08),
                  fontsize=10.5, color=GRAPHITE, fontweight="bold", ha="left", va="center",
                  arrowprops=dict(arrowstyle="-", color=AMBER, lw=1.8),
                  bbox=dict(boxstyle="round,pad=0.42", fc=AMBER_LIGHT, ec="none"))
    ax1.text(10.0, 13.78, "PEAK PRODUCTION\n13,218 units", ha="center", va="bottom",
             fontsize=10, color=TEAL_DARK, fontweight="bold")

    # Panel 2: the benchmark label lives in the dedicated header key.
    p2 = outer[0, 1].subgridspec(2, 1, height_ratios=[0.24, 0.76], hspace=0.02)
    panel_header(fig, p2[0], "02", "Defect rates by production line",
                 "Annual weighted rates • July: Line 2 5.83%; Lines 1 and 3 2.51%",
                 key=(GRAPHITE, (0, (3, 3)), "Overall 2.58%"))
    ax2 = fig.add_subplot(p2[1])
    style_plot(ax2, xgrid=True)
    y = np.arange(len(line_names))
    ax2.barh(y, line_rates, color=[AMBER, TEAL, TEAL], height=0.48, zorder=2)
    ax2.set_yticks(y, [f"{name}\n{units:,} units" for name, units in zip(line_names, line_units)])
    ax2.invert_yaxis()
    ax2.set_xlim(0, 4.1)
    ax2.set_xticks([0, 1, 2, 3], ["0%", "1%", "2%", "3%"])
    ax2.axvline(overall_defect_rate, color=GRAPHITE, linestyle=(0, (3, 3)), linewidth=1.4)
    for yi, rate, defects_count in zip(y, line_rates, line_defects):
        ax2.text(rate + 0.06, yi, f"{rate:.2f}%  •  {defects_count:,} defects",
                 va="center", fontsize=10.5, fontweight="bold", color=GRAPHITE)

    # Panel 3: a clear evidence trail with its own banner and card spacing.
    p3 = outer[1, 0].subgridspec(2, 1, height_ratios=[0.24, 0.76], hspace=0.02)
    panel_header(fig, p3[0], "03", "Duplicate supplier payment screen",
                 "Repeated references require review; matching records do not establish fraud")
    ax3 = fig.add_subplot(p3[1])
    ax3.set_facecolor(PANEL)
    ax3.axis("off")
    ax3.add_patch(FancyBboxPatch((0.025, 0.73), 0.95, 0.20,
                                 boxstyle="round,pad=0.014,rounding_size=0.025",
                                 fc=AMBER_LIGHT, ec="none", transform=ax3.transAxes))
    ax3.text(0.06, 0.845, "1 REPEATED SUPPLIER REFERENCE", transform=ax3.transAxes,
             color=AMBER, fontsize=13, fontweight="bold", va="center")
    ax3.text(0.06, 0.775,
             f"{duplicate_supplier}  •  V01-2025-007  •  same invoice date and amount",
             transform=ax3.transAxes, color=GRAPHITE, fontsize=10.5, va="center")
    ax3.text(0.50, 0.675, "MATCHED AMOUNT  •  PAID ONE DAY APART", transform=ax3.transAxes,
             ha="center", va="center", fontsize=10, color=AMBER, fontweight="bold")
    for idx, (row, cx) in enumerate(zip(duplicate_rows, [0.04, 0.53]), 1):
        ax3.add_patch(FancyBboxPatch((cx, 0.25), 0.43, 0.34,
                                     boxstyle="round,pad=0.018,rounding_size=0.025",
                                     fc=WHITE, ec=GRID, lw=1.1, transform=ax3.transAxes))
        ax3.text(cx + 0.03, 0.525, f"PAID RECORD {idx}", transform=ax3.transAxes,
                 color=TEAL_DARK, fontsize=10, fontweight="bold")
        ax3.text(cx + 0.03, 0.435, f"${row['amount']:,.0f}", transform=ax3.transAxes,
                 color=GRAPHITE, fontsize=24, fontweight="bold")
        ax3.text(cx + 0.03, 0.355, row["invoice_id"], transform=ax3.transAxes,
                 color=GRAPHITE, fontsize=10)
        ax3.text(cx + 0.03, 0.285,
                 f"Invoice {row['invoice_date']}  •  Paid {row['payment_date']}",
                 transform=ax3.transAxes, color=MUTED, fontsize=9.5)
    ax3.text(0.05, 0.12, "CONTROL COMPARISON", transform=ax3.transAxes,
             color=MUTED, fontsize=9.5, fontweight="bold")
    ax3.text(0.05, 0.045,
             "0 invoices with multiple payments  •  0 invoice-level overpayments",
             transform=ax3.transAxes, color=GRAPHITE, fontsize=10)

    # Panel 4: the reference key and summary caption are outside the plot.
    p4 = outer[1, 1].subgridspec(3, 1, height_ratios=[0.24, 0.56, 0.20], hspace=0.10)
    panel_header(fig, p4[0], "04", "Fabric efficiency",
                 "Standard metres ÷ actual metres; higher is better",
                 key=(GRAPHITE, (0, (3, 3)), "100% standard"))
    ax4 = fig.add_subplot(p4[1])
    style_plot(ax4, xgrid=True)
    y4 = np.arange(len(style_names))
    base = 92.0
    ax4.barh(y4, fabric_efficiency - base, left=base,
             color=[AMBER, TEAL, TEAL, TEAL], height=0.48, zorder=2)
    ax4.set_yticks(y4, [f"{pid}  {name}" for pid, name in zip(product_ids, style_names)])
    ax4.invert_yaxis()
    ax4.set_xlim(base, 102.0)
    ax4.set_xticks([92, 94, 96, 98, 100], ["92%", "94%", "96%", "98%", "100%"])
    ax4.axvline(100, color=GRAPHITE, linestyle=(0, (3, 3)), linewidth=1.4)
    for yi, eff, excess in zip(y4, fabric_efficiency, excess_fabric):
        ax4.text(eff + 0.13, yi, f"{eff:.1f}%  •  +{excess:,.1f} m",
                 va="center", fontsize=10.5, color=GRAPHITE, fontweight="bold")
    ax4cap = fig.add_subplot(p4[2])
    ax4cap.axis("off")
    ax4cap.text(0.00, 0.38,
                f"WEIGHTED TOTAL  {weighted_eff:.1f}%", color=TEAL_DARK,
                fontsize=10.5, fontweight="bold", va="center")
    ax4cap.text(0.00, 0.02,
                f"Actual {actual_fabric.sum():,.1f} m  •  Standard {standard_fabric.sum():,.1f} m  •  Excess {excess_fabric.sum():,.1f} m",
                color=MUTED, fontsize=10.2, va="center")

    fig.text(0.05, 0.038,
             "PRELIMINARY SCREENING  |  Indicators support operational follow-up; they do not prove fraud, misconduct or financial-statement misstatement.",
             fontsize=10, color=GRAPHITE, fontweight="bold")
    fig.text(0.05, 0.018,
             "Source: Harbor Stitch Apparel (PostgreSQL), 2025 fictional records • Read-only bounded queries • Exact SQL preserved in the original companion file",
             fontsize=9.2, color=MUTED)

    fig.savefig(PNG, dpi=180, facecolor=WHITE)
    fig.savefig(PDF, facecolor=WHITE)
    plt.close(fig)


if __name__ == "__main__":
    make_dashboard()
    print(f"Wrote {PNG}")
    print(f"Wrote {PDF}")
