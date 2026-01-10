import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Scientific Visualization Dashboard",
    layout="centered"
)

# Title Section
st.markdown(
    """
    <h1 style='text-align: center;'>JIE42403 SCIENTIFIC VISUALIZATION</h1>
    <h2 style='text-align: center;'>PROJECT</h2>
    <h3 style='text-align: center;'>GROUP 5</h3>
    <br>
    <h2 style='text-align: center;'>STUDENT STUDY TECHNIQUES & LEARNING HABITS SURVEY</h2>
    <br>
    """,
    unsafe_allow_html=True
)

# Members Section
st.markdown(
    """
    <h3>Group Members</h3>
    <ul>
        <li><strong>NURUL AINA BINTI MOHD SAHARANI</strong><br>S22A0039</li>
        <li><strong>NAJWATUL INTAN TASNIM BINTI MOHD ANAFI</strong><br>S22A0085</li>
        <li><strong>SHARMINI A/P SELVAM</strong><br>H22A0060</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.info("Please select a page from the sidebar to view each member’s visualization analysis.")


import pandas as pd

# Load dataset
df = pd.read_csv("cleaned_student_study_dataset_FINAL.csv")

st.markdown("---")

# =======================
# STUDY OVERVIEW
# =======================
st.markdown("### 📘 Study Overview")
st.write(
    """
    This dashboard presents insights from a survey-based study 
    exploring students’ study techniques, learning effectiveness, 
    learning challenges, and support needs using scientific visualization.
    """
)

# =======================
# GENERAL PROBLEM STATEMENT
# =======================
st.markdown("### 🚩 General Problem Statement")
st.write(
    """
    Many students face difficulties in their learning process due to uncertainty 
    about effective study techniques, low motivation, and challenges in managing 
    distractions and academic stress. Despite spending time studying, students may 
    still be unsure which learning strategies truly support their academic performance.
    """
)

# =======================
# RESEARCH OBJECTIVES
# =======================
st.markdown("### 🎯 Research Objectives")
st.markdown(
    """
    - To analyze study techniques used by students and their perceived effectiveness  
    - To examine the impact of stress, distraction, and motivation on learning  
    - To explore sleep patterns, learning obstacles, and support needs among students
    """
)

# =======================
# DATASET OVERVIEW
# =======================
st.markdown("### 📊 Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Respondents", len(df))
col2.metric("Survey Sections", 3)
col3.metric("Study Domain", "Education")

# =======================
# SURVEY STRUCTURE
# =======================
st.markdown("### 📝 Survey Structure")
st.markdown(
    """
    - **Part A:** Demographic Information  
    - **Part B:** Study Techniques & Learning Habits  
    - **Part C:** Learning Challenges & Support Needs
    """
)

# =======================
# NAVIGATION HINT
# =======================
st.info("👉 Use the sidebar to explore detailed analysis by each team member.")
