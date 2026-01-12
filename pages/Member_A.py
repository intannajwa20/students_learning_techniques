import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page title & description
# --------------------------------------------------
st.title("📘 Member A: Study Techniques & Learning Effectiveness")

st.markdown(
    """
    **Objective:**  
    To analyse the frequency of study techniques used by students and their
    perceived effectiveness in supporting learning outcomes.
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
# Column groups (readable labels)
# --------------------------------------------------
freq_cols = {
    "Reading Notes / Textbooks": "freq_reading",
    "Watching Online Videos": "freq_online_videos",
    "Practice Tests / Quizzes": "freq_practice_tests",
    "Group Study": "freq_group_study",
    "Summarising Notes": "freq_summarising",
    "Flashcards": "freq_flashcards",
    "Teaching Others": "freq_teaching"
}

eff_cols = {
    "Reading Notes / Textbooks": "eff_reading",
    "Watching Online Videos": "eff_online_videos",
    "Practice Tests / Quizzes": "eff_practice_tests",
    "Group Study": "eff_group_study",
    "Flashcards": "eff_flashcards"
}

# --------------------------------------------------
# 1️⃣ Average Frequency of Study Techniques
# --------------------------------------------------
st.subheader("1️⃣ Average Frequency of Study Techniques Used")

freq_means = pd.DataFrame({
    "Study Technique": list(freq_cols.keys()),
    "Average Frequency": [df[col].mean() for col in freq_cols.values()]
})

fig_freq = px.bar(
    freq_means,
    x="Study Technique",
    y="Average Frequency",
    text="Average Frequency",
    title="Average Frequency of Study Techniques Used"
)

fig_freq.update_traces(texttemplate="%{text:.2f}", textposition="outside")

st.plotly_chart(fig_freq, use_container_width=True)

st.caption(
    "This bar chart shows how often students use different study techniques on average, based on a scale from 1 to 5."
)

st.markdown("""
**Key Insights:**
* Students most frequently rely on traditional methods, such as reading notes/textbooks and watching online videos.

* Active learning strategies like practice tests and teaching others are used less frequently, despite their potential benefits.

* This suggests that many students may prefer passive study techniques over more engaging or cognitively demanding approaches.
""")

st.markdown("---")

# --------------------------------------------------
# 2️⃣ Average Effectiveness of Study Techniques
# --------------------------------------------------
st.subheader("2️⃣ Average Effectiveness of Study Techniques")

eff_means = pd.DataFrame({
    "Study Technique": list(eff_cols.keys()),
    "Average Effectiveness": [df[col].mean() for col in eff_cols.values()]
})

fig_eff = px.bar(
    eff_means,
    x="Study Technique",
    y="Average Effectiveness",
    text="Average Effectiveness",
    title="Average Effectiveness of Study Techniques"
)

fig_eff.update_traces(texttemplate="%{text:.2f}", textposition="outside")

st.plotly_chart(fig_eff, use_container_width=True)

# --------------------------------------------------
# 3️⃣ Grouped Bar Chart: Frequency vs Effectiveness
# --------------------------------------------------
st.subheader("3️⃣ Frequency vs Effectiveness Comparison")

comparison_df = freq_means.merge(
    eff_means, on="Study Technique", how="inner"
)

comparison_long = comparison_df.melt(
    id_vars="Study Technique",
    value_vars=["Average Frequency", "Average Effectiveness"],
    var_name="Metric",
    value_name="Score"
)

fig_grouped = px.bar(
    comparison_long,
    x="Study Technique",
    y="Score",
    color="Metric",
    barmode="group",
    title="Comparison of Frequency and Effectiveness of Study Techniques"
)

st.plotly_chart(fig_grouped, use_container_width=True)

# --------------------------------------------------
# 4️⃣ Heatmap: Usage vs Effectiveness (VALID COMPARISON)
# --------------------------------------------------
st.subheader("4️⃣ Heatmap of Study Technique Usage vs Effectiveness")

freq_series = freq_means.set_index("Study Technique")["Average Frequency"]
eff_series = eff_means.set_index("Study Technique")["Average Effectiveness"]

common_techniques = freq_series.index.intersection(eff_series.index)

heatmap_df = pd.DataFrame({
    "Usage": freq_series.loc[common_techniques],
    "Effectiveness": eff_series.loc[common_techniques]
})

fig_heatmap = px.imshow(
    heatmap_df,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="YlGnBu",
    title="Heatmap of Study Technique Usage vs Effectiveness"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# --------------------------------------------------
# 5️⃣ Box Plot: Distribution of Effectiveness Ratings
# --------------------------------------------------
st.subheader("5️⃣ Distribution of Effectiveness Ratings")

eff_long = df[list(eff_cols.values())].melt(
    var_name="Technique",
    value_name="Effectiveness Score"
)

# Map internal column names to readable labels
eff_long["Technique"] = eff_long["Technique"].map(
    {v: k for k, v in eff_cols.items()}
)

fig_box = px.box(
    eff_long,
    x="Technique",
    y="Effectiveness Score",
    title="Distribution of Effectiveness Ratings by Study Technique"
)

st.plotly_chart(fig_box, use_container_width=True)
