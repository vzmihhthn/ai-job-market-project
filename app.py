
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(layout="wide")

# =========================
# HELPER
# =========================
def show_chart(fig):
    # """Render chart ở 50% width, không bị stretch."""
    col_chart, _ = st.columns([2, 1])
    with col_chart:
        st.pyplot(fig, width='content') 
    plt.close(fig)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/jobs_cleaned.csv")
    # return pd.read_csv("data/processed/jobs_cleaned1.csv")

df = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🔎 Filters")

exp = st.sidebar.multiselect(
    "Experience Level",
    df['experience_level'].unique(),
    default=df['experience_level'].unique()
)

industry = st.sidebar.multiselect(
    "Industry",
    df['industry'].unique(),
    default=df['industry'].unique()
)

remote = st.sidebar.multiselect(
    "Remote Ratio",
    df['remote_ratio'].unique(),
    default=df['remote_ratio'].unique()
)

filtered_df = df[
    (df['experience_level'].isin(exp)) &
    (df['industry'].isin(industry)) &
    (df['remote_ratio'].isin(remote))
].copy()

# =========================
# TITLE
# =========================
st.title("🚀 AI Job Market Dashboard")
st.caption("Analyze how AI is shaping salary, skills, and job trends")

# =========================
# OVERVIEW
# =========================
st.header("📊 Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Avg Salary", f"${int(filtered_df['salary_usd'].mean()):,}")
col3.metric("Avg Experience", round(filtered_df['years_experience'].mean(), 1))

st.info("💡 This section gives a quick snapshot of the job market.")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Salary",
    "🏭 Industry",
    "🌍 Work Style",
    "🤖 Skills"
])

# =========================
# TAB 1: SALARY
# =========================
with tab1:
    st.subheader("Salary by Experience Level")

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    filtered_df.groupby('experience_level')['salary_usd'].mean().plot(kind='bar', ax=ax1)
    ax1.set_xlabel("Experience Level")
    ax1.set_ylabel("Avg Salary (USD)")
    ax1.tick_params(axis='x', rotation=0)
    fig1.tight_layout()
    show_chart(fig1)

    st.markdown("""
    ### 📊 Detailed Explanation:
    - **EN (Entry-level)**: lowest salary group, typically early-career roles.
    - **MI (Mid-level)**: noticeable increase due to skill accumulation.
    - **SE (Senior-level)**: strong jump, reflecting expertise and responsibility.
    - **EX (Executive-level)**: highest salaries due to leadership roles.

    ### 🧠 Key Insight:
    - Salary growth is **not linear** — it accelerates at higher levels.
    - The biggest jump usually occurs between **Mid → Senior → Executive**.

    ### ⚠️ Important Note:
    - This dataset may not reflect real-world perfectly (possible synthetic balance).
    """)
    st.success("👉 Higher experience levels clearly earn significantly more salary.")

    st.subheader("Salary Distribution")

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    filtered_df['salary_usd'].hist(bins=30, ax=ax2)
    ax2.set_xlabel("Salary (USD)")
    ax2.set_ylabel("Count")
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))
    fig2.tight_layout()
    show_chart(fig2)

    st.markdown("""
    ### 📊 Detailed Explanation:
    - This histogram shows how salaries are distributed across all jobs.
    - Most salaries cluster around the **middle range**, with fewer extremely high values.

    ### 🧠 Key Insight:
    - The distribution is typically **right-skewed**: many mid-range salaries, few very high salaries.

    ### ⚠️ Caution:
    - Outliers can distort the average salary.
    """)
    st.info("💡 Most salaries are concentrated in mid-range with some high outliers.")

    st.subheader("Experience vs Salary")

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.scatter(filtered_df['years_experience'], filtered_df['salary_usd'], alpha=0.4, s=10)
    ax3.set_xlabel("Years of Experience")
    ax3.set_ylabel("Salary (USD)")
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))
    fig3.tight_layout()
    show_chart(fig3)

    st.markdown("""
    ### 📊 Detailed Explanation:
    - X-axis: years of experience 
    - Y-axis: salary.

    ### 🧠 Key Insight:
    - **Positive correlation**: more experience → generally higher salary, but not perfectly linear.

    ### ⚠️ Important:
    - Experience alone does NOT determine salary — skills + industry also matter.
    """)
    st.success("👉 Salary increases with experience, but not perfectly linear.")

# =========================
# TAB 2: INDUSTRY
# =========================
with tab2:
    st.subheader("Top Industries")

    col_chart, _ = st.columns([2, 1])
    with col_chart:
        st.bar_chart(filtered_df['industry'].value_counts().head(10))
    st.info("💡 Shows which industries are hiring the most.")

    st.subheader("Top Paying Industries")

    fig4, ax4 = plt.subplots(figsize=(7, 4))
    filtered_df.groupby('industry')['salary_usd'].mean().sort_values(ascending=False).head(10).plot(kind='bar', ax=ax4)
    ax4.set_ylabel("Avg Salary (USD)")
    ax4.tick_params(axis='x', rotation=45)
    plt.setp(ax4.get_xticklabels(), ha='right', rotation_mode='anchor')  # thêm dòng này
    fig4.tight_layout()
    show_chart(fig4)

    st.markdown("""
    ### 📊 Industry Distribution Explanation:
    - This chart shows which industries have the most job postings.
    - Industries appear relatively balanced → dataset may be **synthetic or evenly sampled**.

    ### 💰 Top Paying Industries:
    - Some industries consistently pay more due to higher demand for specialized skills.
    - Tech / Finance often dominate in real-world scenarios.
    """)
    st.success("👉 Some industries pay significantly higher than others.")

# =========================
# TAB 3: WORK STYLE
# =========================
with tab3:
    st.subheader("Remote Work vs Salary")

    fig5, ax5 = plt.subplots(figsize=(7, 4))
    filtered_df.groupby('remote_ratio')['salary_usd'].mean().plot(kind='bar', ax=ax5)
    ax5.set_xlabel("Remote Ratio (%)")
    ax5.set_ylabel("Avg Salary (USD)")
    ax5.tick_params(axis='x', rotation=0)
    fig5.tight_layout()
    show_chart(fig5)

    st.info("💡 Remote work does not drastically change salary levels.")

    st.subheader("Company Size Impact")

    fig6, ax6 = plt.subplots(figsize=(7, 4))
    filtered_df.groupby('company_size')['salary_usd'].mean().plot(kind='bar', ax=ax6)
    ax6.set_xlabel("Company Size")
    ax6.set_ylabel("Avg Salary (USD)")
    ax6.tick_params(axis='x', rotation=0)
    fig6.tight_layout()
    show_chart(fig6)

    st.markdown("""
    ### 🌍 Remote Work Explanation:
    - Salary differences between on-site, hybrid, and fully remote are **relatively small**.
    - Remote work is more about **flexibility than pay**.

    ### 🏢 Company Size Explanation:
    - Larger companies tend to offer **higher salaries** due to more resources and structured roles.
    - Startups may offer lower salary but **higher growth opportunities**.
    """)
    st.success("👉 Larger companies tend to offer higher salaries.")

# =========================
# TAB 4: SKILLS
# =========================
with tab4:
    st.subheader("Top Skills")

    skills_series = filtered_df['required_skills'].dropna().str.lower().str.split(',')
    all_skills = [s.strip() for sub in skills_series for s in sub]
    skill_counts = Counter(all_skills)
    top_skills = pd.DataFrame(skill_counts.most_common(10), columns=['Skill', 'Count'])

    col_chart, _ = st.columns([2, 1])
    with col_chart:
        st.bar_chart(top_skills.set_index('Skill'))
    st.info("💡 These are the most in-demand skills in the job market.")

    st.subheader("Python Skill Impact")

    filtered_df['has_python'] = filtered_df['required_skills'].str.contains('python', na=False, case=False)

    fig7, ax7 = plt.subplots(figsize=(7, 4))
    filtered_df.groupby('has_python')['salary_usd'].mean().plot(kind='bar', ax=ax7)
    ax7.set_xticklabels(['No Python', 'Has Python'], rotation=0)
    ax7.set_ylabel("Avg Salary (USD)")
    fig7.tight_layout()
    show_chart(fig7)

    st.markdown("""
    ### 🤖 Top Skills Explanation:
    - High-demand skills reflect current job market needs and industry trends.
    - Skills appearing frequently = valuable in job market (but frequency ≠ salary impact).

    ### 🐍 Python Impact Explanation:
    - Python-related roles tend to have **higher salaries**.
    - Python is widely used in AI, Data Science, and Automation.

    ### ⚠️ Important:
    - Correlation ≠ causation — high salary may come from role type, not just the skill.
    """)
    st.success("👉 Jobs requiring Python tend to have higher salaries.")

# =========================
# KEY TAKEAWAYS
# =========================
st.header("🧠 Key Takeaways")

st.markdown("""
### 🚀 Final Insights:

1. Salary strongly increases with experience level  
2. Remote work has minimal impact on salary  
3. Skills like Python are associated with higher-paying jobs  
4. Industry differences exist but are relatively balanced  
5. Experience alone does not determine salary — skills and role matter  

### 📌 Overall Conclusion:
The job market shows that **experience and skills are the most important factors**, while work style and industry play a secondary role.
""")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("📌 Note: 2025 data may be incomplete. Results are based on available dataset.")