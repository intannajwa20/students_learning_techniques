import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page title & description
# --------------------------------------------------
st.title("📗 Member B: Distraction, Stress & Motivation")

st.markdown(
    """
    **Objective:**  
    To examine how distractions, stress, and motivation influence students’ learning habits and study behaviors.
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
# Ensure numeric columns are numeric
# --------------------------------------------------
numeric_cols = [
    "limit_distractions",
    "motivation_level",
    "set_study_goals",
    "challenge_lack_of_time",
    "challenge_assignments",
    "challenge_distractions",
    "challenge_environment",
    "challenge_lack_of_motivation"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# 1️⃣ Motivation Level Distribution
# --------------------------------------------------
st.subheader("1️⃣ Motivation Level Distribution")
st.caption("This bar chart shows the distribution of students’ self-reported motivation levels.")

motivation_counts = df["motivation_level"].value_counts().sort_index().reset_index()
motivation_counts.columns = ["Motivation Level", "Count"]

fig_motivation = px.bar(
    motivation_counts,
    x="Motivation Level",
    y="Count",
    text="Count",
    title="Distribution of Student Motivation Levels"
)

fig_motivation.update_traces(textposition="outside")

st.plotly_chart(fig_motivation, use_container_width=True)

st.markdown("""
**Key Insights:**
* Most students report moderate to high motivation levels.
* A smaller group experiences low motivation, which may affect consistent study habits.
""")

st.markdown("---")

# --------------------------------------------------
# 2️⃣ Ability to Limit Distractions
# --------------------------------------------------
st.subheader("2️⃣ Ability to Limit Distractions")
st.caption("This chart illustrates how often students are able to control distractions during study time.")

distraction_counts = df["limit_distractions"].value_counts().sort_index().reset_index()
distraction_counts.columns = ["Ability to Limit Distractions", "Count"]

fig_distraction = px.bar(
    distraction_counts,
    x="Ability to Limit Distractions",
    y="Count",
    text="Count",
    title="Students’ Ability to Limit Distractions"
)

fig_distraction.update_traces(textposition="outside")

st.plotly_chart(fig_distraction, use_container_width=True)

st.markdown("""
**Key Insights:**
* Many students struggle to consistently limit distractions while studying.
* Difficulty in managing distractions may negatively affect focus and learning efficiency.
""")

st.markdown("---")

# --------------------------------------------------
# 3️⃣ Academic Stress Factors
# --------------------------------------------------
st.subheader("3️⃣ Academic Stress Factors")
st.caption(
    "This grouped bar chart compares how frequently students experience different academic stress factors."
)

stress_cols = {
    "Lack of Time": "challenge_lack_of_time",
    "Heavy Assignments": "challenge_assignments",
    "Distractions": "challenge_distractions",
    "Study Environment": "challenge_environment",
    "Lack of Motivation": "challenge_lack_of_motivation"
}

stress_means = pd.DataFrame({
    "Stress Factor": stress_cols.keys(),
    "Average Stress Level": [df[col].mean() for col in stress_cols.values()]
})

fig_stress = px.bar(
    stress_means,
    x="Stress Factor",
    y="Average Stress Level",
    text="Average Stress Level",
    title="Average Frequency of Academic Stress Factors"
)

fig_stress.update_traces(texttemplate="%{text:.2f}", textposition="outside")

st.plotly_chart(fig_stress, use_container_width=True)

st.markdown("""
**Key Insights:**
* Lack of time and heavy assignments are the most frequently reported sources of academic stress.
* Environmental distractions and low motivation also contribute significantly to student stress.
""")

st.markdown("---")

# --------------------------------------------------
# 4️⃣ Motivation vs Distraction Relationship
# --------------------------------------------------
st.subheader("4️⃣ Motivation vs Distraction Relationship")
st.caption(
    "This scatter plot explores the relationship between students’ motivation levels and their ability to limit distractions."
)

scatter_df = df.dropna(subset=["motivation_level", "limit_distractions"])

fig_scatter = px.scatter(
    scatter_df,
    x="motivation_level",
    y="limit_distractions",
    trendline="ols",
    title="Relationship Between Motivation Level and Ability to Limit Distractions",
    labels={
        "motivation_level": "Motivation Level",
        "limit_distractions": "Ability to Limit Distractions"
    }
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
**Key Insights:**
* Students with higher motivation levels tend to report better ability to manage distractions.
* This suggests that motivation may play an important role in maintaining study focus.
""")

st.markdown("---")

# --------------------------------------------------
# 5️⃣ Goal-Setting Frequency
# --------------------------------------------------
st.subheader("5️⃣ Study Goal-Setting Frequency")
st.caption(
    "This chart shows how frequently students set specific goals for their study sessions."
)

likert_order = ["Never", "Rarely", "Sometimes", "Often", "Always"]

goal_counts = (
    df["set_study_goals"]
    .value_counts()
    .reindex(likert_order)
    .reset_index()
)

goal_counts.columns = ["Goal-Setting Frequency", "Count"]

fig_goals = px.bar(
    goal_counts,
    x="Goal-Setting Frequency",
    y="Count",
    text="Count",
    title="Frequency of Study Goal-Setting"
)

fig_goals.update_traces(textposition="outside")

st.plotly_chart(fig_goals, use_container_width=True)

st.markdown("""
**Key Insights:**
* Many students do not consistently set study goals.
* Regular goal-setting may help improve motivation and reduce stress during study sessions.
""")

st.markdown("---")


# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member B)")

st.markdown(
    """
    The findings indicate that distractions, academic stress, and motivation are closely interconnected.
    While many students report moderate to high motivation, challenges such as lack of time, heavy coursework,
    and difficulty managing distractions remain significant barriers to effective learning.
    Strengthening motivation and encouraging structured study behaviors, such as goal-setting,
    may help students better manage stress and improve focus.
    """
)
