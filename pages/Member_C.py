import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page title & description
# --------------------------------------------------
st.title("📙 Member C: Sleep, Obstacles & Support Needs")

st.markdown(
    """
    **Objective:**  
    To explore students’ sleep patterns, learning obstacles, and support needs in order
    to understand how lifestyle factors and support systems influence learning effectiveness.
    """
)

st.divider()

# --------------------------------------------------
# Load dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_habits.csv")

df = load_data()

# --------------------------------------------------
# Ensure numeric columns are numeric (for challenges)
# --------------------------------------------------
numeric_cols = [
    "challenge_health",
    "challenge_understanding",
    "challenge_internet_device"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# 1️⃣ Sleep Duration Distribution
# --------------------------------------------------
st.subheader("1️⃣ Sleep Duration Distribution")
st.caption(
    "This bar chart shows the distribution of students’ average sleep duration per night."
)

sleep_order = [
    "Less than 4 hours",
    "4–5 hours",
    "6–7 hours",
    "8–9 hours",
    "More than 9 hours"
]

sleep_counts = (
    df["sleep_hours"]
    .value_counts()
    .reindex(sleep_order)
    .reset_index()
)

sleep_counts.columns = ["Sleep Duration", "Count"]

fig_sleep = px.bar(
    sleep_counts,
    x="Sleep Duration",
    y="Count",
    text="Count",
    title="Distribution of Students’ Sleep Duration"
)

fig_sleep.update_traces(textposition="outside")

st.plotly_chart(fig_sleep, use_container_width=True)


st.markdown("""
**Key Insights:**
* Most students report sleeping between 6–7 hours per night.
* A noticeable proportion of students experience insufficient sleep, which may affect concentration and learning effectiveness.
""")

st.markdown("---")

# --------------------------------------------------
# 2️⃣ Learning Obstacles (Health, Understanding, Internet/Device)
# --------------------------------------------------
st.subheader("2️⃣ Learning Obstacles")
st.caption(
    "This bar chart compares the average frequency of different learning obstacles experienced by students."
)

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
    title="Average Frequency of Learning Obstacles"
)

fig_obstacles.update_traces(texttemplate="%{text:.2f}", textposition="outside")

st.plotly_chart(fig_obstacles, use_container_width=True)

st.markdown("""
**Key Insights:**
* Difficulty understanding course material is the most prominent learning obstacle.
* Health-related and internet/device issues also contribute to learning challenges for some students.
""")

st.markdown("---")

# --------------------------------------------------
# 3️⃣ Distribution of Learning Obstacles
# --------------------------------------------------
st.subheader("3️⃣ Distribution of Learning Obstacle Levels")
st.caption(
    "This box plot shows the distribution of students’ ratings for different learning obstacles."
)

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
* Some obstacles show greater variability, indicating that their impact differs across students.
* This suggests that learning challenges are not experienced uniformly and may require targeted support.
""")

st.markdown("---")

# --------------------------------------------------
# 4️⃣ Support Needs Distribution
# --------------------------------------------------
st.subheader("4️⃣ Support Needs Distribution")
st.caption(
    "This bar chart shows the most commonly requested types of academic and personal support among students."
)

# Split multi-select support needs
support_series = (
    df["support_needs"]
    .dropna()
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
    title="Distribution of Students’ Support Needs"
)

st.plotly_chart(fig_support, use_container_width=True)

st.markdown("""
**Key Insights:**
* Academic support such as study materials, consultation with lecturers, and peer study groups are commonly requested.
* Mental health and time management support also emerge as important needs, highlighting the role of holistic student support systems.
""")

st.markdown("---")

# --------------------------------------------------
# 5️⃣ Sleep vs Learning Obstacles
# --------------------------------------------------
st.subheader("5️⃣ Sleep Duration vs Learning Obstacles")
st.caption(
    "This chart compares average learning obstacle levels across different sleep duration groups."
)

sleep_obstacle_df = df.groupby("sleep_hours")[list(obstacle_cols.values())].mean().reset_index()

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
    title="Learning Obstacles by Sleep Duration"
)

st.plotly_chart(fig_sleep_obstacle, use_container_width=True)

st.markdown("""
**Key Insights:**
* Students with shorter sleep durations tend to report higher levels of learning obstacles.
* Adequate sleep appears to be associated with reduced learning difficulties.
""")

st.markdown("---")

# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member C)")

st.markdown(
    """
    The findings suggest that lifestyle factors, particularly sleep duration, play an important role
    in students’ learning experiences. Insufficient sleep and learning obstacles such as difficulty
    understanding material and health issues can negatively affect learning effectiveness.
    Furthermore, students express a strong need for both academic and well-being support,
    highlighting the importance of comprehensive support systems in educational environments.
    """
)
