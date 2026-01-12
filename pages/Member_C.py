import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

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
# Load dataset (strip column names)
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_student_study_habits.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --------------------------------------------------
# Normalize sleep_hours for consistent grouping (for static charts)
# --------------------------------------------------
def normalize_sleep(x):
    if pd.isna(x):
        return None
    x = str(x).lower().strip().replace("–", "-")
    x = " ".join(x.split())  # collapse weird spaces
    if "less" in x:
        return "Less than 4 hours"
    if "more" in x:
        return "More than 9 hours"
    if "4" in x and "5" in x:
        return "4-5 hours"
    if "6" in x and "7" in x:
        return "6-7 hours"
    if "8" in x and "9" in x:
        return "8-9 hours"
    return None

df["sleep_hours_clean"] = df.get("sleep_hours", pd.Series([None] * len(df))).apply(normalize_sleep)

sleep_order = ["Less than 4 hours", "4-5 hours", "6-7 hours", "8-9 hours", "More than 9 hours"]

# --------------------------------------------------
# Ensure numeric columns are numeric (for obstacles)
# --------------------------------------------------
numeric_cols = ["challenge_health", "challenge_understanding", "challenge_internet_device"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ==================================================
# 1️⃣ Sleep Duration Distribution (STATIC like Colab)
# ==================================================
st.subheader("1️⃣ Sleep Duration Distribution (Static)")
st.caption("Static chart (Matplotlib) to match Colab output exactly.")

sleep_counts = (
    df["sleep_hours_clean"]
    .dropna()
    .value_counts()
    .reindex(sleep_order, fill_value=0)
)

fig1, ax1 = plt.subplots(figsize=(7, 4))
sleep_counts.plot(kind="bar", ax=ax1)
ax1.set_title("Distribution of Students' Sleep Duration")
ax1.set_xlabel("Sleep Duration")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=30)
st.pyplot(fig1)

st.markdown("""
**Key Insights:**
* Most students sleep between 6–7 hours per night.
* A notable proportion report sleeping less than 5 hours, which may affect focus and learning effectiveness.
""")

st.markdown("---")

# ==================================================
# 2️⃣ Learning Obstacles (INTERACTIVE)
# ==================================================
st.subheader("2️⃣ Learning Obstacles (Interactive)")
st.caption("Interactive bar chart comparing average severity of different learning obstacles.")

obstacle_cols = {
    "Health Issues": "challenge_health",
    "Difficulty Understanding Material": "challenge_understanding",
    "Internet / Device Issues": "challenge_internet_device"
}

# keep only columns that exist
obstacle_cols = {k: v for k, v in obstacle_cols.items() if v in df.columns}

obstacle_means = pd.DataFrame({
    "Obstacle": list(obstacle_cols.keys()),
    "Average Level": [df[v].mean() for v in obstacle_cols.values()]
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
* Difficulty understanding course material is the most prominent obstacle.
* Health and internet/device issues affect a subset of students.
""")

st.markdown("---")

# ==================================================
# 3️⃣ Distribution of Learning Obstacle Levels (INTERACTIVE)
# ==================================================
st.subheader("3️⃣ Distribution of Learning Obstacle Levels (Interactive)")
st.caption("Interactive box plot showing variability in obstacle ratings.")

if obstacle_cols:
    obstacle_long = df[list(obstacle_cols.values())].melt(
        var_name="Obstacle",
        value_name="Level"
    )
    obstacle_long["Obstacle"] = obstacle_long["Obstacle"].map({v: k for k, v in obstacle_cols.items()})

    fig_box = px.box(
        obstacle_long,
        x="Obstacle",
        y="Level",
        title="Distribution of Learning Obstacle Levels"
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("""
**Key Insights:**
* Obstacles vary across students (wide spread in some categories).
* This suggests the need for targeted support rather than one-size-fits-all solutions.
""")

st.markdown("---")

# ==================================================
# 4️⃣ Support Needs Distribution (INTERACTIVE)
# ==================================================
st.subheader("4️⃣ Support Needs Distribution (Interactive)")
st.caption("Interactive bar chart of the most commonly requested support types.")

if "support_needs" in df.columns:
    support_series = (
        df["support_needs"]
        .dropna()
        .astype(str)
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
        text="Count",
        title="Distribution of Students’ Support Needs"
    )
    fig_support.update_traces(textposition="outside")
    st.plotly_chart(fig_support, use_container_width=True)

st.markdown("""
**Key Insights:**
* Time management and mental health support are frequently requested.
* Academic support (materials, lecturer consultation, peer groups) remains important.
""")

st.markdown("---")

# ==================================================
# 5️⃣ Sleep Duration vs Learning Obstacles (STATIC like Colab)
# ==================================================
st.subheader("5️⃣ Sleep Duration vs Learning Obstacles (Static)")
st.caption("Static grouped bar chart (Matplotlib) to match Colab-style output.")

if obstacle_cols:
    grouped = (
        df.dropna(subset=["sleep_hours_clean"])
        .groupby("sleep_hours_clean")[list(obstacle_cols.values())]
        .mean()
        .reindex(sleep_order)
    )

    fig5, ax5 = plt.subplots(figsize=(9, 5))
    grouped.plot(kind="bar", ax=ax5)
    ax5.set_title("Learning Obstacles by Sleep Duration")
    ax5.set_xlabel("Sleep Duration")
    ax5.set_ylabel("Average Level")
    ax5.tick_params(axis="x", rotation=25)
    ax5.legend(title="Obstacle", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig5)

st.markdown("""
**Key Insights:**
* Students with shorter sleep durations generally show higher obstacle levels.
* Adequate sleep appears associated with reduced learning difficulties.
""")

st.markdown("---")

# ==================================================
# Conclusion
# ==================================================
st.subheader("Conclusion (Member C)")

st.markdown("""
Sleep duration is closely linked to students’ learning experiences. Students with insufficient sleep tend to report
higher learning obstacles, particularly difficulty understanding material. The support-needs results also show that
students require both academic and well-being support, highlighting the importance of holistic support systems.
""")
