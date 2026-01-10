import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Member A – Study Techniques & Effectiveness",
    layout="wide"
)

st.title("Study Techniques & Learning Effectiveness")
st.markdown("""
**Objective:**  
To analyze the frequency and perceived effectiveness of different study techniques used by students.
""")

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_student_study_dataset_FINAL.csv")

df = load_data()

st.subheader("1️⃣ Average Frequency of Study Techniques")

freq_cols = [
    "freq_reading","freq_videos","freq_practice","freq_group",
    "freq_summary","freq_flashcards","freq_teaching"
]

freq_means = df[freq_cols].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(freq_means.index, freq_means.values)
ax.set_ylabel("Mean Frequency Score (1–5)")
ax.set_title("Average Frequency of Study Techniques")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig)

st.caption(
    "This chart shows how frequently students use different study techniques on average."
)


st.subheader("2️⃣ Perceived Effectiveness of Study Techniques")

eff_cols = [
    "eff_reading","eff_practice","eff_group",
    "eff_flashcards","eff_videos"
]

eff_means = df[eff_cols].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(eff_means.index, eff_means.values)
ax.set_ylabel("Mean Effectiveness Score (1–5)")
ax.set_title("Perceived Effectiveness of Study Techniques")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig)

st.caption(
    "This visualization highlights which study techniques students perceive as most effective."
)

st.subheader("3️⃣ Relationship Between Frequency and Effectiveness")

corr_cols = [
    "freq_reading","freq_practice","freq_group",
    "eff_reading","eff_practice","eff_group"
]

corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Between Frequency and Effectiveness")

st.pyplot(fig)

st.caption(
    "The heatmap shows how the frequency of using certain techniques relates to their perceived effectiveness."
)


st.subheader("4️⃣ Study Preference: Alone vs With Others")

pref_counts = df["study_preference"].value_counts()

fig, ax = plt.subplots(figsize=(4,4))
ax.pie(
    pref_counts.values,
    labels=pref_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
ax.set_title("Study Preference Distribution")

st.pyplot(fig)

st.caption(
    "This chart shows whether students prefer studying alone or in groups."
)


st.subheader("5️⃣ Preferred Study Time")

time_counts = df["study_time"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))
ax.bar(time_counts.index, time_counts.values)
ax.set_ylabel("Number of Students")
ax.set_xlabel("Study Time")
ax.set_title("Preferred Study Time")

st.pyplot(fig)

st.caption(
    "This bar chart illustrates when students most commonly choose to study."
)


st.markdown("---")
st.subheader("Key Insights")

st.markdown("""
- Students tend to rely more on certain study techniques, such as reading notes and group study.
- Techniques perceived as more effective are not always the most frequently used.
- A positive relationship exists between the frequent use of some techniques and their effectiveness.
- Study preferences and study time vary, suggesting the need for flexible learning strategies.
""")
