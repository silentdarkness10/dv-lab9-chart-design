"""TFB3133/TEB3133 Data Visualization - Lab 9: Design Principles and Chartjunk.

Run locally:  streamlit run lab9.py

All sales figures are FICTIONAL practice values.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Lab 9 | Chart Design", layout="wide")

# ---------------------------------------------------------------- data ----
# Assignment Part 2: branch names and values changed from the lab example, and
# Part 3: two more categories added (Selangor, Perak) -> six branches in total.
ALL_DATA = pd.DataFrame({
    "Branch": ["Penang", "Johor", "Sabah", "Sarawak", "Selangor", "Perak"],
    "Sales": [94, 97, 96, 99, 100, 95],
})

SOURCE_NOTE = ("Data: fictional practice values (2026) | "
               "Chart: Muhammad Muzammil Bin Mohamed Imtiaz")

# ------------------------------------------------------------- controls ----
st.title("Designing a Clearer Bar Chart")
version = st.radio("Choose a chart", ["Cluttered", "Improved"], horizontal=True)
n_branches = st.radio("Number of branches", [4, 6], index=1, horizontal=True,
                      help="Six branches is the final version. Choose 4 to see "
                           "the original-size chart.")

data = ALL_DATA.head(n_branches).reset_index(drop=True)
top = data.loc[data["Sales"].idxmax()]

fig, ax = plt.subplots(figsize=(8, 4.5))

if version == "Cluttered":
    # Deliberately bad: truncated axis, rainbow colours, grey background,
    # heavy grid, shouting title, no value labels.
    rainbow = ["#8FB9A8", "#D8B365", "#B2ABD2", "#5E3C99", "#C51B7D", "#1B9E77"]
    bars = ax.bar(data["Branch"], data["Sales"], color=rainbow[:n_branches])
    ax.set_ylim(data["Sales"].min() - 1, data["Sales"].max() + 1)  # truncated
    ax.set_facecolor("#E8E8E8")
    ax.grid(True, which="both", color="white", linewidth=2)
    ax.set_title("SALES PERFORMANCE!!!")
else:
    bars = ax.bar(data["Branch"], data["Sales"], color="#4C78A8")
    for branch, bar in zip(data["Branch"], bars):
        if branch == top["Branch"]:
            bar.set_color("#E07A3F")          # one accent colour = one message
    ax.set_ylim(0, 110)                        # zero baseline for a bar chart
    ax.set_yticks(range(0, 101, 20))           # natural increments
    ax.bar_label(bars, fmt="%.0f", padding=3)  # labels, so colour is not the only cue
    ax.set_title(f"{top['Branch']} branch recorded the highest sales", loc="left")
    # Removed (extra element for Part 2): the horizontal grid lines. Every bar is
    # labelled with its value and the axis starts at zero, so the grid no longer
    # adds information.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

ax.set_ylabel("Sales (units)")
ax.set_xlabel("Branch")

# Attribution on the chart itself (design standard 10) - improved view only,
# so the cluttered view stays a faithful "before".
if version == "Improved":
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=8, color="#555555", ha="left")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
else:
    fig.tight_layout()

st.pyplot(fig, clear_figure=True)

# ------------------------------------------------------- explanation ----
lo, hi = data["Sales"].min(), data["Sales"].max()
if version == "Cluttered":
    shown_axis_min = lo - 1
    apparent = (hi - shown_axis_min) / (lo - shown_axis_min)
    actual = hi / lo
    st.warning(
        f"**Why this misleads:** the axis starts at {shown_axis_min}, not 0. "
        f"The tallest bar looks about **{apparent:.0f}x** as tall as the shortest, "
        f"but the real ratio is only **{actual:.2f}x** ({hi} vs {lo} units)."
    )
else:
    st.success(
        f"**How to read this:** bar length is proportional to sales because the "
        f"axis starts at 0. The highest branch ({top['Branch']}, {top['Sales']}) is "
        f"only {(hi / lo - 1) * 100:.1f}% above the lowest ({lo})."
    )

st.caption("Fictional practice data. The improved bar chart starts at zero. "
           + SOURCE_NOTE)
