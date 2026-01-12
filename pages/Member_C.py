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
# Load dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_habits.csv")

df = load_data()

# --------------------------------------------------
# 🔧 CRITICAL FIX: Standardize sleep_hours categories
# --------------------------------------------------
df["sleep_hours"] = (
    df["sleep_hours"]
    .astype(str)
    .str.strip()
    .str.replace("–", "-", regex=False)  # normalize dash
)

sleep_order = [
    "Less than 4 hours",
    "4-5 hours",
    "6-7 hours",
    "8-9 hours",
    "More than 9 hours"
]

# --------------------------------------------------
# Ensure numeric columns are numeric
# --------------------------------------------------
numeric_cols = [
    "challenge_health",
    "challenge_understanding",
    "challenge_internet_device"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==================================================
# 1️⃣ Sleep Duration Distribution
# ==================================================
st.subheader("1️⃣ Sleep Duration Distribution")
st.caption("This bar chart shows the distribution of students’ average sleep duration per night.")

sleep_counts = (
    df["sleep_hours"]
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

st.markdown("""
**Key Insights:**
* Most students sleep between 6–7 hours per night.
* A notable proportion of students report sleeping less than 5 hours, which may negatively impact learning effectiveness.
""")

st.markdown("---")

# ==================================================
# 2️⃣ Learning Obstacles (Average Level)
# ==================================================
st.subheader("2️⃣ Learning Obstacles")
st.caption("This chart compares the average severity of different learning obstacles experienced by students.")

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

st.markdown("""
**Key Insights:**
* Difficulty understanding course material is the most significant learning obstacle.
* Health and internet/device issues also affect a subset of students.
""")

st.markdown("---")

# ==================================================
# 3️⃣ Distribution of Learning Obstacle Levels
# ==================================================
st.subheader("3️⃣ Distribution of Learning Obstacle Levels")
st.caption("This box plot shows the variability of students’ ratings for different learning obstacles.")

obstacle_long = df[list(obstacle_cols.values())].melt(
    var_name="Obstacle",
    value_name="Level"
)

obstacle_long["Obstacle"] = obstacle_long["Obstacle"].map(
    {v: k for k, v in obstacle_cols.items()}
)

fig_box_obstacles = px.box(
    obstacle_long,
    x="Obstacle",
    y="Level",
    title="Distribution of Learning Obstacle Levels"
)

st.plotly_chart(fig_box_obstacles, use_container_width=True)

st.markdown("""
**Key Insights:**
* Some obstacles show wide variability, indicating different impacts across students.
* Learning challenges are not experienced uniformly and may require targeted support.
""")

st.markdown("---")

# ==================================================
# 4️⃣ Support Needs Distribution
# ==================================================
st.subheader("4️⃣ Support Needs Distribution")
st.caption("This chart shows the most frequently requested academic and personal support services.")

support_series = (
    df["support_needs"]
    .dropna()
    .str.split(", ")
    .explode()
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

st.markdown("""
**Key Insights:**
* Time management guidance and mental health support are among the most requested needs.
* Academic support such as study materials and lecturer consultation remains highly important.
""")

st.markdown("---")

# ==================================================
# 5️⃣ Sleep Duration vs Learning Obstacles
# ==================================================
st.subheader("5️⃣ Sleep Duration vs Learning Obstacles")
st.caption("This grouped bar chart compares learning obstacle levels across different sleep duration groups.")

sleep_obstacle_df = (
    df.groupby("sleep_hours")[list(obstacle_cols.values())]
    .mean()
    .reindex(sleep_order)
    .reset_index()
)

sleep_obstacle_long = sleep_obstacle_df.melt(
    id_vars="sleep_hours",
    var_name="Obstacle",
    value_name="Average Level"
)

sleep_obstacle_long["Obstacle"] = sleep_obstacle_long["Obstacle"].map(
    {v: k for k, v in obstacle_cols.items()}
)

fig_sleep_obstacle = px.bar(
    sleep_obstacle_long,
    x="sleep_hours",
    y="Average Level",
    color="Obstacle",
    barmode="group",
    title="Learning Obstacles by Sleep Duration",
    category_orders={"sleep_hours": sleep_order}
)

st.plotly_chart(fig_sleep_obstacle, use_container_width=True)

st.markdown("""
**Key Insights:**
* Students with shorter sleep durations generally report higher learning obstacle levels.
* Adequate sleep appears to be associated with fewer learning difficulties.
""")

st.markdown("---")

# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member C)")

st.markdown("""
Overall, the analysis indicates that sleep duration plays a critical role in students’ learning experiences.
Insufficient sleep is associated with higher learning obstacles, particularly difficulty understanding course material.
In addition, students express strong demand for both academic and well-being support services.
These findings highlight the importance of promoting healthy sleep habits and comprehensive support systems
to enhance learning effectiveness.
""")
