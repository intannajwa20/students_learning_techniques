import streamlit as st
import pandas as pd
import plotly.express as px

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
# Load dataset (CRITICAL FIX INCLUDED)
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_student_study_habits.csv")
    df.columns = df.columns.str.strip()  # 🔥 FIX: remove hidden spaces
    return df

df = load_data()

# --------------------------------------------------
# HARD CLEAN sleep_hours (RULE-BASED & SAFE)
# --------------------------------------------------
def normalize_sleep(x):
    if pd.isna(x):
        return None
    x = str(x).lower().strip()

    if "less" in x:
        return "Less than 4 hours"
    elif "4" in x and "5" in x:
        return "4-5 hours"
    elif "6" in x and "7" in x:
        return "6-7 hours"
    elif "8" in x and "9" in x:
        return "8-9 hours"
    elif "more" in x:
        return "More than 9 hours"
    else:
        return None

df["sleep_hours_clean"] = df["sleep_hours"].apply(normalize_sleep)

sleep_order = [
    "Less than 4 hours",
    "4-5 hours",
    "6-7 hours",
    "8-9 hours",
    "More than 9 hours"
]

# --------------------------------------------------
# Ensure numeric obstacle columns
# --------------------------------------------------
numeric_cols = [
    "challenge_health",
    "challenge_understanding",
    "challenge_internet_device"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==================================================
# 1️⃣ Sleep Duration Distribution  ✅ FIXED
# ==================================================
st.subheader("1️⃣ Sleep Duration Distribution")

sleep_counts = (
    df["sleep_hours_clean"]
    .value_counts()
    .reindex(sleep_order, fill_value=0)
    .reset_index()
)

sleep_counts.columns = ["Sleep Duration", "Count"]

fig_sleep = px.bar(
    sleep_counts,
    x="Sleep Duration",
    y="Count",
    text="Count",
    title="Distribution of Students’ Sleep Duration",
    category_orders={"Sleep Duration": sleep_order}
)

fig_sleep.update_traces(textposition="outside")

st.plotly_chart(fig_sleep, use_container_width=True)

st.markdown("---")

# ==================================================
# 2️⃣ Learning Obstacles (Average Level)
# ==================================================
st.subheader("2️⃣ Learning Obstacles")

obstacle_cols = {
    "Health Issues": "challenge_health",
    "Difficulty Understanding Material": "challenge_understanding",
    "Internet / Device Issues": "challenge_internet_device"
}

obstacle_means = pd.DataFrame({
    "Obstacle": obstacle_cols.keys(),
    "Average Level": [df[col].mean() for col in obstacle_cols.values()]
})

fig_obstacles = px.bar(
    obstacle_means,
    x="Obstacle",
    y="Average Level",
    text="Average Level",
    title="Average Severity of Learning Obstacles"
)

fig_obstacles.update_traces(texttemplate="%{text:.2f}", textposition="outside")

st.plotly_chart(fig_obstacles, use_container_width=True)

st.markdown("---")

# ==================================================
# 3️⃣ Distribution of Learning Obstacle Levels
# ==================================================
st.subheader("3️⃣ Distribution of Learning Obstacle Levels")

obstacle_long = df[list(obstacle_cols.values())].melt(
    var_name="Obstacle",
    value_name="Level"
)

obstacle_long["Obstacle"] = obstacle_long["Obstacle"].map(
    {v: k for k, v in obstacle_cols.items()}
)

fig_box = px.box(
    obstacle_long,
    x="Obstacle",
    y="Level",
    title="Distribution of Learning Obstacle Levels"
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")

# ==================================================
# 4️⃣ Support Needs Distribution
# ==================================================
st.subheader("4️⃣ Support Needs Distribution")

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

fig_support = px.bar(
    support_counts,
    x="Support Type",
    y="Count",
    text="Count",
    title="Distribution of Students’ Support Needs"
)

fig_support.update_traces(textposition="outside")

st.plotly_chart(fig_support, use_container_width=True)

st.markdown("---")

# ==================================================
# 5️⃣ Sleep Duration vs Learning Obstacles ✅ FIXED
# ==================================================
st.subheader("5️⃣ Sleep Duration vs Learning Obstacles")

sleep_obstacle_df = (
    df.groupby("sleep_hours_clean")[list(obstacle_cols.values())]
    .mean()
    .reindex(sleep_order)
    .reset_index()
)

sleep_obstacle_long = sleep_obstacle_df.melt(
    id_vars="sleep_hours_clean",
    var_name="Obstacle",
    value_name="Average Level"
)

sleep_obstacle_long["Obstacle"] = sleep_obstacle_long["Obstacle"].map(
    {v: k for k, v in obstacle_cols.items()}
)

fig_sleep_obstacle = px.bar(
    sleep_obstacle_long,
    x="sleep_hours_clean",
    y="Average Level",
    color="Obstacle",
    barmode="group",
    title="Learning Obstacles by Sleep Duration",
    category_orders={"sleep_hours_clean": sleep_order}
)

st.plotly_chart(fig_sleep_obstacle, use_container_width=True)

st.markdown("---")

# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member C)")

st.markdown("""
Sleep duration plays a critical role in students’ learning experiences.
Students with insufficient sleep tend to report higher learning obstacles,
particularly in understanding course material.
Additionally, strong demand for academic and well-being support highlights
the need for holistic student support systems.
""")
