import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Study Techniques & Learning Behaviors",
    page_icon="📘",
    layout="wide"
)

# --------------------------------------------------
# Load dataset (cached for performance)
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_habits.csv")

df = load_data()

# --------------------------------------------------
# HOME PAGE CONTENT
# --------------------------------------------------

st.title("📘 Study Overview")

st.markdown(
    """
    This interactive dashboard presents insights from a **survey-based study**
    exploring students’ study techniques, learning effectiveness, academic challenges,
    and support needs using **scientific data visualization**.
    """
)

st.divider()

# --------------------------------------------------
# Problem Statement
# --------------------------------------------------
st.header("🚩 General Problem Statement")

st.markdown(
    """
    Many students face difficulties in their learning process due to uncertainty
    about effective study techniques, low motivation, and challenges in managing
    distractions and academic stress. Despite spending time studying, students may
    still be unsure which learning strategies truly support their academic performance.
    """
)

# --------------------------------------------------
# Research Objectives
# --------------------------------------------------
st.header("🎯 Research Objectives")

st.markdown(
    """
    - To analyze the **frequency and perceived effectiveness** of different study techniques used by students.
    - To examine **stress, distraction, and motivation levels** and the relationships between these factors.
    - To explore **sleep patterns, learning obstacles, and support needs** that influence learning effectiveness.
    """
)

# --------------------------------------------------
# Dataset Overview (Key Metrics)
# --------------------------------------------------
st.header("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Respondents",
        value=df.shape[0]
    )

with col2:
    st.metric(
        label="Survey Sections",
        value="3"
    )

with col3:
    st.metric(
        label="Study Domain",
        value="Education"
    )

st.divider()

# --------------------------------------------------
# Navigation Hint
# --------------------------------------------------
st.subheader("📂 Navigate the Dashboard")

st.markdown(
    """
    Use the **sidebar on the left** to explore:
    - **Dataset Overview** – demographics and background information
    - **Member A** – Study techniques & learning effectiveness
    - **Member B** – Stress, distraction & motivation
    - **Member C** – Sleep patterns, obstacles & support needs
    """
)

st.info("💡 Tip: All visualizations are interactive. Hover, zoom, and explore the charts for deeper insights.")
