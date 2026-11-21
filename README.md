# Employee Tenure Distribution Analysis

A Streamlit multi-page HR analytics project with a shared responsive CSS theme across the home page and all seven modules. Existing employee data, analysis, charts, filters, and CSV exports are preserved.

## Pages
1. Overview
2. Employee Directory
3. Tenure Analysis
4. Department Analysis
5. Attrition Analysis
6. Hiring Trends
7. Reports & Downloads

## Run on Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The shared styling is defined in `common.py` (`apply_css`) and is loaded by every page.
