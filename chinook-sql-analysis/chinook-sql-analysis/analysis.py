"""
Chinook SQL Sales Analysis
==========================
Runs all SQL queries against the Chinook SQLite database,
renders results as tables, and produces publication-quality charts.

Usage:
    python analysis.py
"""

import sqlite3
import os
import pathlib
import textwrap

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR  = pathlib.Path(__file__).parent
DB_PATH   = BASE_DIR / "data" / "chinook.db"
QUERY_DIR = BASE_DIR / "queries"
OUT_DIR   = BASE_DIR / "outputs"
VIZ_DIR   = BASE_DIR / "visualizations"
OUT_DIR.mkdir(exist_ok=True)
VIZ_DIR.mkdir(exist_ok=True)

PALETTE = ["#2563EB","#7C3AED","#DB2777","#D97706","#059669",
           "#0891B2","#DC2626","#65A30D","#9333EA","#EA580C"]

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(sql: str) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn)


def run_file(filename: str) -> pd.DataFrame:
    path = QUERY_DIR / filename
    with open(path) as f:
        raw = f.read()
    # Strip comment lines for execution
    lines = [l for l in raw.splitlines() if not l.strip().startswith("--")]
    sql = "\n".join(lines).strip()
    return run_query(sql)


def save_csv(df: pd.DataFrame, name: str):
    path = OUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"   💾  Saved {path.name}")


def section(title: str):
    print("\n" + "═" * 60)
    print(f"  {title}")
    print("═" * 60)


# ── Chart Helpers ─────────────────────────────────────────────────────────────
def bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename,
              color=None, top_n=15, horizontal=False):
    df = df.head(top_n).copy()
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [color or PALETTE[i % len(PALETTE)] for i in range(len(df))]

    if horizontal:
        df = df.iloc[::-1]  # flip so highest is on top
        bars = ax.barh(df[x_col], df[y_col], color=colors)
        ax.set_xlabel(ylabel, fontsize=11)
        ax.set_ylabel(xlabel, fontsize=11)
        for bar in bars:
            w = bar.get_width()
            ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                    f"${w:,.0f}", va="center", fontsize=8)
    else:
        bars = ax.bar(df[x_col], df[y_col], color=colors)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        plt.xticks(rotation=35, ha="right", fontsize=9)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h * 1.01,
                    f"${h:,.0f}", ha="center", fontsize=8)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    path = VIZ_DIR / filename
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊  Saved {path.name}")


def line_chart(df, x_col, y_col, title, xlabel, ylabel, filename, color="#2563EB"):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df[x_col], df[y_col], color=color, linewidth=2.5, marker="o",
            markersize=4, markerfacecolor="white", markeredgewidth=1.5)
    ax.fill_between(df[x_col], df[y_col], alpha=0.12, color=color)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    step = max(1, len(df) // 12)
    ax.set_xticks(range(0, len(df), step))
    ax.set_xticklabels(df[x_col].iloc[::step], rotation=35, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    path = VIZ_DIR / filename
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊  Saved {path.name}")


def pie_chart(df, label_col, value_col, title, filename, top_n=8):
    df = df.head(top_n).copy()
    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        df[value_col], labels=None, autopct="%1.1f%%",
        colors=PALETTE[:len(df)], startangle=140,
        pctdistance=0.82, wedgeprops=dict(width=0.6)
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax.legend(wedges, df[label_col], loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    path = VIZ_DIR / filename
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊  Saved {path.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS SECTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def q1_top_tracks():
    section("Q1 · Top-Selling Tracks by Revenue")
    df = run_file("01_top_selling_tracks.sql")
    print(df[["TrackName","Artist","Genre","TimesSold","TotalRevenue"]].head(10).to_string(index=False))
    save_csv(df, "01_top_selling_tracks")
    bar_chart(df, "TrackName", "TotalRevenue",
              "Top 20 Best-Selling Tracks by Revenue",
              "Track", "Revenue (USD)",
              "01_top_tracks.png", horizontal=True)
    return df


def q2_revenue_by_region():
    section("Q2 · Revenue per Region (Country)")
    df = run_file("02_revenue_per_region.sql")
    print(df[["Country","TotalInvoices","UniqueCustomers","TotalRevenue","RevenueSharePct"]].head(15).to_string(index=False))
    save_csv(df, "02_revenue_per_region")
    bar_chart(df, "Country", "TotalRevenue",
              "Total Revenue by Country",
              "Country", "Revenue (USD)",
              "02_revenue_by_country.png", top_n=15)
    pie_chart(df, "Country", "TotalRevenue",
              "Revenue Share by Country (Top 8)",
              "02_revenue_share_pie.png")
    return df


def q3_monthly_performance():
    section("Q3 · Monthly Revenue Performance")
    df = run_file("03_monthly_performance.sql")
    print(df[["YearMonth","TotalOrders","UniqueCustomers","MonthlyRevenue","MoM_Change"]].head(12).to_string(index=False))
    save_csv(df, "03_monthly_performance")
    line_chart(df, "YearMonth", "MonthlyRevenue",
               "Monthly Revenue Trend (2022–2024)",
               "Month", "Revenue (USD)",
               "03_monthly_revenue.png")
    # Order volume
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(range(len(df)), df["TotalOrders"], color=PALETTE[2], alpha=0.85)
    step = max(1, len(df) // 12)
    ax.set_xticks(range(0, len(df), step))
    ax.set_xticklabels(df["YearMonth"].iloc[::step], rotation=35, ha="right", fontsize=9)
    ax.set_title("Monthly Order Volume", fontsize=13, fontweight="bold")
    ax.set_ylabel("Orders")
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "03_monthly_orders.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊  Saved 03_monthly_orders.png")
    return df


def q4_genre_revenue():
    section("Q4 · Revenue by Genre")
    df = run_file("04_genre_revenue.sql")
    print(df[["Genre","TrackCount","TimesSold","TotalRevenue","RevenueSharePct"]].to_string(index=False))
    save_csv(df, "04_genre_revenue")
    bar_chart(df, "Genre", "TotalRevenue",
              "Revenue by Music Genre",
              "Genre", "Revenue (USD)",
              "04_genre_revenue.png", top_n=12)
    return df


def q5_top_customers():
    section("Q5 · Top Customers by Lifetime Value")
    df = run_file("05_top_customers.sql")
    print(df[["CustomerName","Country","TotalOrders","LifetimeValue","SupportRep"]].head(10).to_string(index=False))
    save_csv(df, "05_top_customers")
    bar_chart(df, "CustomerName", "LifetimeValue",
              "Top 20 Customers by Lifetime Value",
              "Customer", "Lifetime Value (USD)",
              "05_top_customers.png", horizontal=True)
    return df


def q6_artist_performance():
    section("Q6 · Artist Sales Performance")
    df = run_file("06_artist_performance.sql")
    print(df[["Artist","AlbumCount","TrackCount","TimesSold","TotalRevenue"]].head(10).to_string(index=False))
    save_csv(df, "06_artist_performance")
    bar_chart(df, "Artist", "TotalRevenue",
              "Top Artists by Revenue",
              "Artist", "Revenue (USD)",
              "06_artist_revenue.png", top_n=15, horizontal=True)
    return df


def q7_sales_rep():
    section("Q7 · Sales Rep Performance")
    df = run_file("07_sales_rep_performance.sql")
    print(df.to_string(index=False))
    save_csv(df, "07_sales_rep_performance")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(df["SalesRep"], df["TotalRevenue"],
                color=PALETTE[:len(df)])
    axes[0].set_title("Total Revenue by Rep", fontweight="bold")
    axes[0].set_ylabel("Revenue (USD)")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    axes[0].tick_params(axis="x", rotation=15)

    axes[1].bar(df["SalesRep"], df["CustomersSupported"],
                color=PALETTE[3:3+len(df)])
    axes[1].set_title("Customers Supported by Rep", fontweight="bold")
    axes[1].set_ylabel("Customers")
    axes[1].tick_params(axis="x", rotation=15)

    for ax in axes:
        ax.spines[["top","right"]].set_visible(False)
    plt.suptitle("Sales Rep Performance Dashboard", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "07_sales_rep.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊  Saved 07_sales_rep.png")
    return df


def q8_customer_cohort():
    section("Q8 · Customer Cohort Segmentation")
    df = run_file("08_customer_cohort.sql")
    print(df.to_string(index=False))
    save_csv(df, "08_customer_cohort")
    pie_chart(df, "Segment", "SegmentRevenue",
              "Revenue Share by Customer Segment",
              "08_customer_segments.png", top_n=4)
    return df


def summary_dashboard(results: dict):
    """Build a single-page KPI overview chart."""
    section("Building Summary Dashboard")

    monthly = results["monthly"]
    region  = results["region"]
    genre   = results["genre"]
    tracks  = results["tracks"]

    fig = plt.figure(figsize=(18, 12))
    fig.patch.set_facecolor("#F8FAFC")
    fig.suptitle("Chinook Music Store — Sales Analytics Dashboard",
                 fontsize=18, fontweight="bold", y=0.98)

    gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.4)

    # KPI Boxes
    total_rev   = monthly["MonthlyRevenue"].sum()
    total_orders = monthly["TotalOrders"].sum()
    avg_order   = total_rev / total_orders if total_orders else 0
    top_country = region.iloc[0]["Country"]

    kpis = [
        (f"${total_rev:,.0f}", "Total Revenue"),
        (f"{int(total_orders):,}", "Total Orders"),
        (f"${avg_order:.2f}", "Avg Order Value"),
        (f"{top_country}", "Top Market"),
    ]
    kpi_colors = ["#2563EB","#7C3AED","#DB2777","#D97706"]
    for idx, (val, label) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, idx if idx < 3 else idx - 3])
        ax.set_facecolor(kpi_colors[idx % 4])
        ax.text(0.5, 0.6, val, transform=ax.transAxes,
                ha="center", va="center", fontsize=20, fontweight="bold",
                color="white")
        ax.text(0.5, 0.2, label, transform=ax.transAxes,
                ha="center", va="center", fontsize=11, color="#EFF6FF")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)

    # Monthly trend
    ax_trend = fig.add_subplot(gs[1, :])
    ax_trend.set_facecolor("#FFFFFF")
    ax_trend.plot(range(len(monthly)), monthly["MonthlyRevenue"],
                  color="#2563EB", linewidth=2.5)
    ax_trend.fill_between(range(len(monthly)), monthly["MonthlyRevenue"],
                          alpha=0.15, color="#2563EB")
    step = max(1, len(monthly) // 12)
    ax_trend.set_xticks(range(0, len(monthly), step))
    ax_trend.set_xticklabels(monthly["YearMonth"].iloc[::step],
                              rotation=30, ha="right", fontsize=8)
    ax_trend.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax_trend.set_title("Monthly Revenue Trend", fontweight="bold")
    ax_trend.spines[["top","right"]].set_visible(False)

    # Top 8 countries
    ax_ctry = fig.add_subplot(gs[2, :2])
    ax_ctry.set_facecolor("#FFFFFF")
    top8 = region.head(8)
    bars = ax_ctry.barh(top8["Country"][::-1], top8["TotalRevenue"][::-1],
                        color=PALETTE[:8])
    ax_ctry.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax_ctry.set_title("Revenue by Country (Top 8)", fontweight="bold")
    ax_ctry.spines[["top","right"]].set_visible(False)

    # Genre donut
    ax_genre = fig.add_subplot(gs[2, 2])
    ax_genre.set_facecolor("#FFFFFF")
    top6g = genre.head(6)
    ax_genre.pie(top6g["TotalRevenue"], labels=top6g["Genre"],
                 autopct="%1.0f%%", colors=PALETTE[:6],
                 pctdistance=0.82,
                 wedgeprops=dict(width=0.55), startangle=140,
                 textprops={"fontsize": 8})
    ax_genre.set_title("Revenue by Genre", fontweight="bold")

    path = VIZ_DIR / "00_dashboard.png"
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"   📊  Saved {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n🎵  Chinook SQL Sales Analysis")
    print("=" * 60)

    r_tracks  = q1_top_tracks()
    r_region  = q2_revenue_by_region()
    r_monthly = q3_monthly_performance()
    r_genre   = q4_genre_revenue()
    r_cust    = q5_top_customers()
    r_artist  = q6_artist_performance()
    r_rep     = q7_sales_rep()
    r_cohort  = q8_customer_cohort()

    summary_dashboard({
        "monthly": r_monthly,
        "region":  r_region,
        "genre":   r_genre,
        "tracks":  r_tracks,
    })

    print("\n" + "═" * 60)
    print("✅  Analysis complete!")
    print(f"   CSV results  → {OUT_DIR}")
    print(f"   Visualizations → {VIZ_DIR}")
    print("═" * 60)
