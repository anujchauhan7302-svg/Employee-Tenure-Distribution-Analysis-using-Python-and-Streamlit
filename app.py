import streamlit as st
from common import load_data, page_header, metric_row, apply_css

st.set_page_config(page_title="Employee Tenure Analytics", page_icon="👥", layout="wide")
apply_css()

df=load_data()
page_header("Employee Tenure Distribution Analysis","A multi-page HR analytics portal to explore workforce strength, service duration and employee movement.")
st.subheader("Dashboard Overview")
metric_row(df)
st.write("")
left,right=st.columns([1.3,1])
with left:
    st.subheader("Explore the project")
    st.markdown("""
    Use the **page navigation in the left sidebar** to open each module:
    - **Overview** – key workforce indicators and quick insights
    - **Employee Directory** – search, filter and download employee records
    - **Tenure Analysis** – service-duration distribution and tenure groups
    - **Department Analysis** – compare departments and their workforce
    - **Attrition Analysis** – analyze employees who left the company
    - **Hiring Trends** – explore joining patterns by year and month
    - **Reports** – export filtered and complete analysis reports
    """)
with right:
    st.subheader("Dataset snapshot")
    st.write(f"**Departments:** {df['department'].nunique()}")
    st.write(f"**First joining date:** {df['joining_date'].min().date()}")
    st.write(f"**Latest joining date:** {df['joining_date'].max().date()}")
    st.write(f"**Dataset records:** {len(df):,}")
st.info("Select a page from the sidebar to begin exploring the analytics.")
