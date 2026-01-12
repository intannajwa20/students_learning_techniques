import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page title & description
# --------------------------------------------------
st.title("📙 Member C: Sleep, Learning Obstacles & Support Needs")

st.markdown("""
**Objective:**  
To explore sleep patterns, learning obstacles, and support needs among students
in order to understand how lifestyle factors and institutional support
influence learning effectiveness.
""")

st.divider()

# --------------------------------------------------
# Load dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_habits.csv")

df = load_data()

# ==================================================
# 1️⃣ Sleep Duration Distribution
# ==================================================
st.subheader("1️⃣ Sleep Duration Distribution")
st.caption("This chart shows the distribution of students’ average sleep duration per night.")

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
* A noticeable group reports sleeping less than 5 hours, indicating possible sleep deprivation.
* Very few students achieve more than 8 hours of sleep consistently.
""")

st.markdown("---")

# ==================================================
# 2️⃣ Sleep Adequacy Distribution
# ==================================================
st.subheader("2️⃣ Sleep Adequacy Distribution")
st.caption("Students’ perceived adequacy of sleep (1 = Very low, 5 = Very high).")

df["sleep_adequacy_level"] = pd.to_numeric(
    df["sleep_adequacy_level"], errors="coerce"
)

likert_levels = [1, 2, 3, 4, 5]

sleep_adequacy_counts = (
    df["sleep_adequacy_level"]
    .value_counts()
    .reindex(likert_levels, fill_value=0)
    .reset_index()
)

sleep_adequacy_counts.columns = ["Sleep Adequacy Level", "Number of Students"]

fig_sleep_adequacy = px.bar(
    sleep_adequacy_counts,
    x="Sleep Adequacy Level",
    y="Number of Students",
    text="Number of Students",
    title="Distribution of Students’ Sleep Adequacy",
    category_orders={"Sleep Adequacy Level": likert_levels}
)

fig_sleep_adequacy.update_traces(textposition="outside")
st.plotly_chart(fig_sleep_adequacy, use_container_width=True)

st.markdown("""
**Key Insights:**
* Most students rate their sleep adequacy as moderate (levels 2–3).
* Only a small number report very high sleep adequacy.
* This suggests sleep quality may be a concern for many students.
""")

st.markdown("---")

# ==================================================
# 3️⃣ Learning Obstacles
# ==================================================
st.subheader("3️⃣ Learning Obstacles")
st.caption("Average severity of learning obstacles faced by students.")

obstacle_cols = {
    "Lack of Time": "challenge_lack_of_time",
    "Understanding Course Content": "challenge_understanding",
    "Internet / Device Issues": "challenge_internet_device",
    "Health Issues": "challenge_health"
}

# Ensure numeric
for col in obstacle_cols.values():
    df[col] = pd.to_numeric(df[col], errors="coerce")

obstacle_means = pd.DataFrame({
    "Learning Obstacle": obstacle_cols.keys(),
    "Average Severity": [df[col].mean() for col in obstacle_cols.values()]
})

fig_obstacles = px.bar(
    obstacle_means,
    x="Learning Obstacle",
    y="Average Severity",
    text="Average Severity",
    title="Average Severity of Learning Obstacles"
)

fig_obstacles.update_traces(texttemplate="%{text:.2f}", textposition="outside")
st.plotly_chart(fig_obstacles, use_container_width=True)

st.markdown("""
**Key Insights:**
* Lack of time is the most significant learning obstacle.
* Difficulties in understanding course content also affect many students.
* Health and technical issues, while less dominant, still impact learning.
""")

st.markdown("---")

# ==================================================
# 4️⃣ Student Support Needs
# ==================================================
st.subheader("4️⃣ Student Support Needs")
st.caption("Frequency of different types of support requested by students.")

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
    title="Student Support Needs"
)

fig_support.update_traces(textposition="outside")
st.plotly_chart(fig_support, use_container_width=True)

st.markdown("""
**Key Insights:**
* Time management guidance and mental health support are among the most requested.
* Academic support such as study materials and lecturer consultations remain important.
* Support needs reflect both academic and well-being challenges faced by students.
""")

st.markdown("---")

# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member C)")

st.markdown("""
Overall, the findings indicate that many students experience moderate sleep adequacy
and face significant challenges related to time management and learning obstacles.
The high demand for academic and mental health support highlights the importance
of holistic student support systems to improve learning effectiveness and well-being.
""")
