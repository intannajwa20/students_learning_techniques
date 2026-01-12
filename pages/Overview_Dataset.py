import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page title
# --------------------------------------------------
st.title("📊 Dataset Overview")

st.markdown(
    """
    This page provides an **interactive overview** of the cleaned survey dataset,
    allowing users to explore respondent demographics and study background.
    """
)

st.divider()

# --------------------------------------------------
# Load dataset (cached)
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_habits.csv")

df = load_data()

# --------------------------------------------------
# BASIC DATASET METRICS
# --------------------------------------------------
st.header("📌 Key Dataset Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Respondents", df.shape[0])

with col2:
    st.metric("Total Variables", df.shape[1])

with col3:
    st.metric("Study Domain", "Education")

st.divider()

# --------------------------------------------------
# INTERACTIVE FILTERS
# --------------------------------------------------
st.header("🔍 Filter Respondents")

col1, col2, col3 = st.columns(3)

with col1:
    gender_filter = st.multiselect(
        "Select Gender",
        options=df["gender"].unique(),
        default=df["gender"].unique()
    )

with col2:
    level_filter = st.multiselect(
        "Select Level of Study",
        options=df["level_of_study"].unique(),
        default=df["level_of_study"].unique()
    )

with col3:
    programme_filter = st.multiselect(
        "Select Programme / Major",
        options=df["programme"].unique(),
        default=df["programme"].unique()
    )

# Apply filters
filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["level_of_study"].isin(level_filter)) &
    (df["programme"].isin(programme_filter))
]

st.info(f"🔎 Showing **{filtered_df.shape[0]}** respondents after filtering.")

st.divider()

# --------------------------------------------------
# GENDER DISTRIBUTION
# --------------------------------------------------
st.subheader("👤 Gender Distribution")

gender_counts = filtered_df["gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]

fig_gender = px.bar(
    gender_counts,
    x="Gender",
    y="Count",
    text="Count",
    title="Gender Distribution of Respondents",
)

fig_gender.update_traces(textposition="outside")

st.plotly_chart(fig_gender, use_container_width=True)

# --------------------------------------------------
# LEVEL OF STUDY DISTRIBUTION
# --------------------------------------------------
st.subheader("🎓 Level of Study Distribution")

level_counts = filtered_df["level_of_study"].value_counts().reset_index()
level_counts.columns = ["Level of Study", "Count"]

fig_level = px.bar(
    level_counts,
    x="Level of Study",
    y="Count",
    text="Count",
    title="Respondents by Level of Study",
)

fig_level.update_traces(textposition="outside")

st.plotly_chart(fig_level, use_container_width=True)

# --------------------------------------------------
# PROGRAMME / MAJOR DISTRIBUTION
# --------------------------------------------------
st.subheader("📚 Programme / Major Distribution")

programme_counts = (
    filtered_df["programme"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Programme", "programme": "Count"})
)

fig_programme = px.bar(
    programme_counts,
    x="Programme",
    y="Count",
    title="Respondents by Programme / Major"
)

st.plotly_chart(fig_programme, use_container_width=True)

# --------------------------------------------------
# INTERACTIVE DATA PREVIEW
# --------------------------------------------------
st.subheader("📄 Survey Dataset Preview")

st.markdown(
    "You can scroll, sort, and explore the cleaned survey dataset below."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

