"""
06_eda_charts.py — Stage 7.2
Six charts for the HR attrition case study.

Run once:  py python\analysis\06_eda_charts.py
Output:    python\outputs\charts\*.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------
# Paths + global style
# ------------------------------------------------------------------
BASE    = r"C:\Users\Anonymous\Desktop\projects\03-HR Analytics Case"
IN_DIR  = f"{BASE}\\data\\processed"
OUT_DIR = f"{BASE}\\python\\outputs\\charts"
os.makedirs(OUT_DIR, exist_ok=True)

BENCHMARK = 16.12
RED       = "#c0392b"
GRAY      = "#7f8c8d"
BLUE      = "#2c3e50"

plt.rcParams.update({
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":        True,
    "axes.grid.axis":   "y",
    "grid.color":       "#ecf0f1",
    "figure.facecolor": "white",
})

# ------------------------------------------------------------------
# Load + prep (once)
# ------------------------------------------------------------------
master = pd.read_csv(f"{IN_DIR}\\hr_master_clean.csv")
att    = pd.read_csv(f"{IN_DIR}\\attendance_employee_summary.csv")

master["tenure_band"] = master["tenure_band"].str.replace(" years", "", regex=False)
master["attrition_flag"] = (master["attrition"] == "Yes").astype(int)

def hours_band(h):
    if pd.isna(h): return None
    if h < 7.5:    return "Short"
    if h < 8.0:    return "Normal"
    return "Long"

att["hours_band"] = att["avg_hours"].apply(hours_band)
df = master.merge(att[["employee_id", "avg_hours", "hours_band"]],
                  on="employee_id", how="left")


def add_benchmark(ax):
    """Draw the 16.12% company benchmark as a dashed line."""
    ax.axhline(BENCHMARK, color=GRAY, linestyle="--", linewidth=1.2,
               label=f"Company benchmark ({BENCHMARK}%)")


# ==================================================================
# CHART 1 — Attrition by department
# ==================================================================
def chart01_department():
    order = ["Human Resources", "Research & Development", "Sales"]
    g = (df[df["department"].isin(order)]
         .groupby("department")
         .agg(n=("employee_id", "size"),
              leavers=("attrition_flag", "sum")))
    g["rate"] = 100.0 * g["leavers"] / g["n"]
    g = g.reindex(order)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(g.index, g["rate"], color=RED, width=0.6, zorder=2)
    add_benchmark(ax)

    for bar, (_, row) in zip(bars, g.iterrows()):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.6,
                f"{row['rate']:.2f}%\n(n={row['n']:,}, leavers={row['leavers']})",
                ha="center", va="bottom", fontsize=10)

    ax.set_ylabel("Attrition rate (%)")
    ax.set_title("Attrition by Department")
    ax.set_ylim(0, max(g["rate"].max() + 6, BENCHMARK + 6))
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}\\chart01_attrition_by_department.png", dpi=150)
    plt.close(fig)


# ==================================================================
# CHART 2 — Attrition by tenure band
# ==================================================================
def chart02_tenure():
    order = ["0-1", "2-3", "4-5", "6-10", "10+"]
    g = (df.groupby("tenure_band")
         .agg(n=("employee_id", "size"),
              leavers=("attrition_flag", "sum")))
    g["rate"] = 100.0 * g["leavers"] / g["n"]
    g = g.reindex(order)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(g.index, g["rate"], color=RED, width=0.6, zorder=2)
    add_benchmark(ax)

    for bar, (_, row) in zip(bars, g.iterrows()):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.6,
                f"{row['rate']:.2f}%\n(n={row['n']:,})",
                ha="center", va="bottom", fontsize=10)

    ax.set_xlabel("Tenure band (years at company)")
    ax.set_ylabel("Attrition rate (%)")
    ax.set_title("Attrition by Tenure — Monotonic Decline")
    ax.set_ylim(0, g["rate"].max() + 6)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}\\chart02_attrition_by_tenure.png", dpi=150)
    plt.close(fig)


# ==================================================================
# CHART 3 — Attrition by satisfaction dimension
# ==================================================================
def chart03_satisfaction():
    # Three dimensions, each with its natural low->high order
    dims = {
        "Environment Satisfaction": ("environment_satisfaction",
                                     ["Low", "Medium", "High", "Very High"]),
        "Job Satisfaction":         ("job_satisfaction",
                                     ["Low", "Medium", "High", "Very High"]),
        "Work-Life Balance":        ("work_life_balance",
                                     ["Bad", "Good", "Better", "Best"]),
    }
    # Map codes to labels for env/job (1-4) and WLB (1-4)
    label_map = {1: None, 2: None, 3: None, 4: None}

    fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=True)

    for ax, (title, (col, labels)) in zip(axes, dims.items()):
        # Row count by code
        counts = df[col].value_counts().sort_index()
        leavers = df.groupby(col)["attrition_flag"].sum().sort_index()
        rates = 100.0 * leavers / counts

        # Drop NaNs (null satisfaction preserved, not imputed)
        valid = rates.dropna()
        xs = labels[:len(valid)]

        bars = ax.bar(xs, valid.values, color=RED, width=0.6, zorder=2)
        ax.axhline(BENCHMARK, color=GRAY, linestyle="--", linewidth=1.2)

        for bar, (code, rate) in zip(bars, valid.items()):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.6,
                    f"{rate:.2f}%\n(n={int(counts[code]):,})",
                    ha="center", va="bottom", fontsize=9)

        ax.set_title(title, fontsize=12)
        ax.set_ylim(0, max(valid.max() + 7, BENCHMARK + 7))
        ax.tick_params(axis="x", rotation=15)

    axes[0].set_ylabel("Attrition rate (%)")
    fig.suptitle("Attrition by Satisfaction Dimension (lower = higher risk)",
                 fontsize=14, fontweight="bold", y=1.00)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}\\chart03_attrition_by_satisfaction.png", dpi=150)
    plt.close(fig)


# ==================================================================
# CHART 4 — Tenure x hours heatmap (CENTERPIECE)
# ==================================================================
def chart04_heatmap():
    tenure_order = ["0-1", "2-3", "4-5", "6-10", "10+"]
    hours_order  = ["Short", "Normal", "Long"]

    g = (df.groupby(["tenure_band", "hours_band"])
         .agg(n=("employee_id", "size"),
              leavers=("attrition_flag", "sum")))
    g["rate"] = 100.0 * g["leavers"] / g["n"]

    # Pivot for the heatmap grid
    rate_grid = g["rate"].unstack().reindex(index=tenure_order, columns=hours_order)
    n_grid    = g["n"].unstack().reindex(index=tenure_order, columns=hours_order)
    lv_grid   = g["leavers"].unstack().reindex(index=tenure_order, columns=hours_order)

    fig, ax = plt.subplots(figsize=(9, 6))
    im = ax.imshow(rate_grid.values, cmap="Reds", aspect="auto", vmin=0, vmax=60)

    # Annotate every cell: rate / n / leavers
    for i, t in enumerate(tenure_order):
        for j, h in enumerate(hours_order):
            r = rate_grid.iloc[i, j]
            n = int(n_grid.iloc[i, j]) if not pd.isna(n_grid.iloc[i, j]) else 0
            lv = int(lv_grid.iloc[i, j]) if not pd.isna(lv_grid.iloc[i, j]) else 0
            if n == 0:
                continue
            text = f"{r:.2f}%\n(n={n}, lv={lv})"
            color = "white" if r > 35 else "black"
            ax.text(j, i, text, ha="center", va="center",
                    fontsize=10, color=color, fontweight="bold")

    ax.set_xticks(range(len(hours_order)))
    ax.set_xticklabels(hours_order)
    ax.set_yticks(range(len(tenure_order)))
    ax.set_yticklabels(tenure_order)
    ax.set_xlabel("Average daily hours (Short <7.5h | Normal 7.5-8h | Long 8h+)")
    ax.set_ylabel("Tenure band (years)")
    ax.set_title("Attrition Rate: Tenure × Hours Worked\n(compounding, not overlap)")
    ax.grid(False)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Attrition rate (%)")

    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}\\chart04_tenure_hours_heatmap.png", dpi=150)
    plt.close(fig)


# ==================================================================
# CHART 5 — Year-7 spike inside 6-10 x Long
# ==================================================================
def chart05_year7():
    cell = df[(df["tenure_band"] == "6-10") & (df["hours_band"] == "Long")]

    g = (cell.groupby("years_since_last_promotion")
         .agg(n=("employee_id", "size"),
              leavers=("attrition_flag", "sum")))
    g["rate"] = 100.0 * g["leavers"] / g["n"]
    g = g.sort_index()

    fig, ax = plt.subplots(figsize=(11, 6))
    xs = g.index.astype(int).tolist()
    bars = ax.bar([str(x) for x in xs], g["rate"], color=RED, width=0.7, zorder=2)

    # Highlight the 7-year bar
    for bar, x in zip(bars, xs):
        if x == 7:
            bar.set_color(BLUE)
        bar.set_zorder(2)

    for bar, (yr, row) in zip(bars, g.iterrows()):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.8,
                f"{row['rate']:.1f}%\n(n={row['n']:,})",
                ha="center", va="bottom", fontsize=9)

    ax.set_xlabel("Years since last promotion (raw value)")
    ax.set_ylabel("Attrition rate (%)")
    ax.set_title("Year-7 Spike: Attrition Inside 6-10 yrs Tenure × Long Hours\n"
                 "(the '4+ years promotion' band was a coarse-banding artifact)")
    ax.set_ylim(0, g["rate"].max() + 8)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}\\chart05_year7_spike.png", dpi=150)
    plt.close(fig)


# ==================================================================
# CHART 6 — High-risk cells x department
# ==================================================================
def chart06_dept_cells():
    df["cell"] = df["tenure_band"] + " × " + df["hours_band"].astype(str)
    cells = ["0-1 × Long", "0-1 × Short", "2-3 × Long",
             "4-5 × Long", "6-10 × Long"]
    depts = ["Research & Development", "Sales", "Human Resources"]

    g = (df[df["cell"].isin(cells) & df["department"].isin(depts)]
         .groupby(["cell", "department"])
         .agg(n=("employee_id", "size"),
              leavers=("attrition_flag", "sum")))
    g["rate"] = 100.0 * g["leavers"] / g["n"]
    # Hide cells with n<20 (per 08d rule)
    g = g[g["n"] >= 20]

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.27
    x = np.arange(len(cells))
    colors = {"Research & Development": RED,
              "Sales": "#e67e22",
              "Human Resources": BLUE}

    for i, dept in enumerate(depts):
        vals, ns = [], []
        for c in cells:
            if (c, dept) in g.index:
                vals.append(g.loc[(c, dept), "rate"])
                ns.append(int(g.loc[(c, dept), "n"]))
            else:
                vals.append(0)
                ns.append(0)
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width, label=dept,
                      color=colors[dept], zorder=2)
        for bar, v, n in zip(bars, vals, ns):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width()/2,
                        v + 0.8, f"{v:.1f}%\n(n={n})",
                        ha="center", va="bottom", fontsize=8)

    add_benchmark(ax)
    ax.set_xticks(x)
    ax.set_xticklabels(cells, rotation=15)
    ax.set_ylabel("Attrition rate (%)")
    ax.set_title("High-Risk Cells × Department (n ≥ 20)\n"
                 "Which department owns which cell?")
    ax.set_ylim(0, 72)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}\\chart06_high_risk_by_department.png", dpi=150)
    plt.close(fig)


# ==================================================================
# Run all
# ==================================================================
if __name__ == "__main__":
    print("Building charts...")
    chart01_department();            print("  1/6 department           ✅")
    chart02_tenure();                print("  2/6 tenure               ✅")
    chart03_satisfaction();          print("  3/6 satisfaction         ✅")
    chart04_heatmap();               print("  4/6 tenure×hours heatmap ✅")
    chart05_year7();                 print("  5/6 year-7 spike         ✅")
    chart06_dept_cells();            print("  6/6 high-risk × dept     ✅")
    print(f"\nDone. Files in: {OUT_DIR}")