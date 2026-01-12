import streamlit as st
import pandas as pd
import plotly.express as px

st.subheader("1️⃣ Sleep Adequacy Distribution")
st.caption(
    "This bar chart shows students’ perceived adequacy of their sleep on a scale from 1 (Very low) to 5 (Very high)."
)

# Ensure numeric
df["sleep_adequacy_level"] = pd.to_numeric(
    df["sleep_adequacy_level"], errors="coerce"
)

# Define Likert scale explicitly
likert_levels = [1, 2, 3, 4, 5]

sleep_adequacy_counts = (
    df["sleep_adequacy_level"]
    .value_counts()
    .reindex(likert_levels, fill_value=0)
    .reset_index()
)

sleep_adequacy_counts.columns = [
    "Sleep Adequacy Level",
    "Number of Students"
]

fig_sleep_adequacy = px.bar(
    sleep_adequacy_counts,
    x="Sleep Adequacy Level",
    y="Number of Students",
    text="Number of Students",
    title="Distribution of Students’ Sleep Adequacy",
    category_orders={"Sleep Adequacy Level": likert_levels}
)

fig_sleep_adequacy.update_traces(textposition="outside")
fig_sleep_adequacy.update_layout(
    xaxis_title="Sleep Adequacy Level (1 = Very low, 5 = Very high)",
    yaxis_title="Number of Students"
)

st.plotly_chart(fig_sleep_adequacy, use_container_width=True)

st.markdown("""
**Key Insights:**
* Most students rate their sleep adequacy at moderate levels (2–3).
* Relatively few students report very high sleep adequacy.
* This suggests that insufficient or inconsistent sleep may be common among students.
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
