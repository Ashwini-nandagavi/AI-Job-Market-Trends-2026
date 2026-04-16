import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Job Market Trends 2026",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("AI_Job_Market_Trends_2026.csv")
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.strip()
    return df

df = load_data()

st.title("🤖 AI Job Market Trends 2026")
st.markdown(f"""
Comprehensive analysis of **{len(df):,}+ AI & Data Science job postings**, revealing:

- 💰 Salary trends across seniority levels and roles  
- 🛠️ Most in-demand skills in the global AI job market  
- 📊 Job category distribution  
- 🏢 Top hiring countries and top job titles  
""")
st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filter Data")

# Job Title Filter
roles = df['job_title'].unique()
selected_roles = st.sidebar.multiselect("Select Job Titles", roles, default=roles[:5])

# Country Filter
countries = df['country'].unique()
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries[:5])

# Salary Range
min_sal = int(df['salary'].min())
max_sal = int(df['salary'].max())
salary_range = st.sidebar.slider("Salary Range", min_sal, max_sal, (min_sal, max_sal))

# Experience Range
min_exp = int(df['years_experience'].min())
max_exp = int(df['years_experience'].max())
experience_range = st.sidebar.slider("Years of Experience", min_exp, max_exp, (min_exp, max_exp))

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df['job_title'].isin(selected_roles)) &
    (df['country'].isin(selected_countries)) &
    (df['salary'].between(salary_range[0], salary_range[1])) &
    (df['years_experience'].between(experience_range[0], experience_range[1]))
]

if filtered_df.empty:
    st.warning("⚠ No data found with the selected filters.")
    st.stop()

# ---------------- KPI METRICS ----------------
st.subheader("📊 Key Insights")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Average Salary", f"${filtered_df['salary'].mean():,.0f}")
col3.metric("Top Country", filtered_df['country'].mode()[0])
col4.metric("Top Job Title", filtered_df['job_title'].mode()[0])

st.divider()

# ---------------- SALARY VISUALS ----------------
st.subheader("💰 Salary Analysis")

c1, c2 = st.columns(2)

with c1:
    fig_sal = px.histogram(filtered_df, x="salary", nbins=30, title="Salary Distribution")
    st.plotly_chart(fig_sal, use_container_width=True)

with c2:
    fig_role_sal = px.box(filtered_df, x="job_title", y="salary", title="Salary by Job Title")
    st.plotly_chart(fig_role_sal, use_container_width=True)

# ---------------- COUNTRY ANALYSIS ----------------
st.subheader("🌍 Country-Level Insights")

c1, c2 = st.columns(2)

with c1:
    country_count = filtered_df['country'].value_counts()
    fig_country = px.bar(
        x=country_count.values,
        y=country_count.index,
        title="Top Hiring Countries",
        orientation='h'
    )
    st.plotly_chart(fig_country, use_container_width=True)

with c2:
    fig_country_pie = px.pie(
        names=country_count.index,
        values=country_count.values,
        title="Country Hiring Share"
    )
    st.plotly_chart(fig_country_pie, use_container_width=True)

# ---------------- EXPERIENCE VS SALARY ----------------
st.subheader("📈 Experience vs Salary")

fig_exp_sal = px.scatter(
    filtered_df,
    x="years_experience",
    y="salary",
    color="job_title",
    size="job_openings",
    hover_data=["company_industry"],
    title="Salary vs Experience"
)
st.plotly_chart(fig_exp_sal, use_container_width=True)

# ---------------- SKILLS ANALYSIS ----------------
st.subheader("🛠 Skills Demand Overview")

skill_cols = ["skills_python", "skills_sql", "skills_ml", "skills_deep_learning", "skills_cloud"]
skill_counts = filtered_df[skill_cols].sum().sort_values(ascending=False)

fig_skills = px.bar(
    x=skill_counts.values,
    y=skill_counts.index,
    orientation='h',
    title="Most In-Demand Skills"
)
st.plotly_chart(fig_skills, use_container_width=True)

# ---------------- JOB OPENINGS ----------------
st.subheader("📌 Job Openings by Role")

fig_openings = px.bar(
    filtered_df,
    x="job_title",
    y="job_openings",
    color="job_title",
    title="Job Openings per Job Title"
)
st.plotly_chart(fig_openings, use_container_width=True)

# ---------------- FOOTER ----------------
st.divider()

