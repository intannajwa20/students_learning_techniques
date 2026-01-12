import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page title & description
# --------------------------------------------------
st.title("📙 Member C: Sleep, Obstacles & Support Needs")

st.markdown("""
**Objective:**  
To explore students’ sleep patterns, learning obstacles, and support needs in order
to understand how lifestyle factors and support systems influence learning effectiveness.
""")

st.divider()

# --------------------------------------------------
# Load dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_habits.csv")

df = load_data()

# --------------------------------------------------
# IMPORTANT: Sleep in cleaned CSV is already numeric (1–5)
# Create sleep_adequacy_level exactly like Colab
# --------------------------------------------------
if "sleep_adequacy_level" not in df.columns:
    # In your Colab: sleep_adequacy_level = sleep_hours
    df["sleep_adequacy_level"] = df.get("sleep_hours")

df["sleep_adequacy_level"] = pd.to_numeric(df["sleep_adequacy_level"], errors="coerce")
if df["sleep_adequacy_level"].isna().all():
    st.error("sleep_adequacy_level is empty (all NaN). Check your cleaned CSV columns.")
    st.stop()

# Fill missing with mode (same idea as Colab)
df["sleep_adequacy_level"] = df["sleep_adequacy_level"].fillna(df["sleep_adequacy_level"].mode()[0])

sleep_levels = [1, 2, 3, 4, 5]

# --------------------------------------------------
# Ensure obstacle columns are numeric (1–5)
# --------------------------------------------------
obstacle_cols = {
    "Health Issues": "challenge_health",
    "Difficulty Understanding Material": "challenge_understanding",
    "Internet / Device Issues": "challenge_internet_device"
}

for col in obstacle_cols.values():
    df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[col].notna().any():
        df[col] = df[col].fillna(df[col].mode()[0])

st.subheader("1️⃣ Distribution of Sleep Adequacy (Interactive)")
st.caption("Interactive bar chart showing students’ sleep adequacy levels (1 = very low, 5 = very high).")

sleep_counts = (
    df["sleep_adequacy_level"]
    .value_counts()
    .sort_index()
    .reset_index()
)

sleep_counts.columns = ["Sleep Adequacy Level", "Count"]

fig_sleep_interactive = px.bar(
    sleep_counts,
    x="Sleep Adequacy Level",
    y="Count",
    text="Count",
    title="Distribution of Students’ Sleep Adequacy",
)

fig_sleep_interactive.update_traces(textposition="outside")

st.plotly_chart(fig_sleep_interactive, use_container_width=True)


st.markdown("""
**Key Insights:**
* Most students cluster around the middle sleep adequacy levels (typically 3–4).
* A smaller group reports low sleep adequacy (1–2), which may reduce focus and learning effectiveness.
""")

st.markdown("---")

# ==================================================
# 2️⃣ (INTERACTIVE) Learning Obstacles (Average Level)
# ==================================================
st.subheader("2️⃣ Learning Obstacles (Average Level)")
st.caption("Interactive: compares average severity of learning obstacles (1 = Never, 5 = Very often).")

obstacle_means = pd.DataFrame({
    "Obstacle": list(obstacle_cols.keys()),
    "Average Level": [df[c].mean() for c in obstacle_cols.values()]
})

fig2 = px.bar(
    obstacle_means,
    x="Obstacle",
    y="Average Level",
    text="Average Level",
    title="Average Severity of Learning Obstacles"
)
fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
**Key Insights:**
* Difficulty understanding material is commonly the strongest obstacle.
* Health and internet/device issues still affect a subset of students.
""")

st.markdown("---")

# ==================================================
# 3️⃣ (INTERACTIVE) Distribution of Learning Obstacle Levels (Box Plot)
# ==================================================
st.subheader("3️⃣ Distribution of Learning Obstacle Levels")
st.caption("Interactive: shows variability of obstacle ratings across students.")

obstacle_long = df[list(obstacle_cols.values())].melt(var_name="Obstacle", value_name="Level")
obstacle_long["Obstacle"] = obstacle_long["Obstacle"].map({v: k for k, v in obstacle_cols.items()})

fig3 = px.box(
    obstacle_long,
    x="Obstacle",
    y="Level",
    title="Distribution of Learning Obstacle Levels"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**Key Insights:**
* Wide boxes/long whiskers mean the obstacle affects students very differently.
* This suggests support should be targeted, not one-size-fits-all.
""")

st.markdown("---")

# ==================================================
# 4️⃣ (INTERACTIVE) Support Needs Distribution
# ==================================================
st.subheader("4️⃣ Support Needs Distribution")
st.caption("Interactive: most frequently requested support services.")

support_series = (
    df["support_needs"]
    .dropna()
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

support_counts = support_series.value_counts().reset_index()
support_counts.columns = ["Support Type", "Count"]

fig4 = px.bar(
    support_counts,
    x="Support Type",
    y="Count",
    text="Count",
    title="Distribution of Students’ Support Needs"
)
fig4.update_traces(textposition="outside")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
**Key Insights:**
* Students request both academic help (materials, lecturer consultation, peer groups)
  and well-being help (mental health/stress, time management).
""")

st.markdown("---")

# ==================================================
# 5️⃣ (STATIC) Stacked Bar: Support Needs Across Sleep Adequacy (Colab style)
# ==================================================
st.subheader("5️⃣ Support Needs Across Sleep Adequacy Levels (Interactive)")
st.caption("Interactive stacked bar chart showing support needs by sleep adequacy level.")

support_sleep = (
    df[["sleep_adequacy_level", "support_needs"]]
    .dropna()
    .assign(support=lambda d: d["support_needs"].astype(str).str.split(","))
    .explode("support")
)

support_sleep["support"] = support_sleep["support"].str.strip()

pivot_support = (
    support_sleep
    .groupby(["sleep_adequacy_level", "support"])
    .size()
    .reset_index(name="Count")
)

fig_support_sleep = px.bar(
    pivot_support,
    x="sleep_adequacy_level",
    y="Count",
    color="support",
    barmode="stack",
    title="Support Needs Across Sleep Adequacy Levels",
    labels={
        "sleep_adequacy_level": "Sleep Adequacy Level (1 = very low, 5 = very high)",
        "support": "Support Type"
    }
)

st.plotly_chart(fig_support_sleep, use_container_width=True)

st.markdown("""
**Key Insights:**
* Support needs appear across all sleep levels, but patterns can differ by group.
* This helps identify which supports might be prioritized for students with lower sleep adequacy.
""")

st.markdown("---")

# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member C)")

st.markdown("""
Overall, sleep adequacy varies across students, and learning obstacles (especially difficulty understanding)
remain a major barrier. Students also highlight strong demand for both academic and well-being support.
Together, these findings suggest that improving learning effectiveness may require *both* better study support
systems and healthier student lifestyles (including sleep).
""")
