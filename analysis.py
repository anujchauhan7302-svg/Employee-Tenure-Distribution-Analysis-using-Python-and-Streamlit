
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================
# STEP 1: READ DATASET
# =====================================

df = pd.read_csv("dataset/employees.csv")

print("Employee Dataset:")
print(df)

# =====================================
# STEP 2: DISPLAY FIRST 5 RECORDS
# =====================================

print("\nFirst 5 Employees:")
print(df.head())

# =====================================
# STEP 3: DATASET INFORMATION
# =====================================

print("\nDataset Information:")
df.info()

# =====================================
# STEP 4: CHECK MISSING VALUES
# =====================================

print("\nMissing Values:")
print(df.isnull().sum())

# =====================================
# STEP 5: CONVERT DATES
# =====================================

df["joining_date"] = pd.to_datetime(
    df["joining_date"], errors="coerce"
)

df["exit_date"] = pd.to_datetime(
    df["exit_date"], errors="coerce"
)

# =====================================
# STEP 6: CALCULATE TENURE
# =====================================

today = pd.Timestamp.today().normalize()

df["end_date"] = df["exit_date"].fillna(today)

df["tenure"] = (
    (df["end_date"] - df["joining_date"]).dt.days / 365.25
)

# =====================================
# STEP 7: EMPLOYEE STATUS
# =====================================

df["status"] = np.where(
    df["exit_date"].isna(),
    "Currently Working",
    "Left Company"
)

# =====================================
# STEP 8: TENURE CATEGORIES
# =====================================

df["tenure_category"] = pd.cut(
    df["tenure"],
    bins=[-0.001, 1, 3, 5, float("inf")],
    labels=[
        "New Employee",
        "Junior Employee",
        "Experienced Employee",
        "Senior Employee"
    ]
)

# =====================================
# STEP 9: DISPLAY EMPLOYEE ANALYSIS
# =====================================

print("\nEmployee Tenure Analysis:")

print(
    df[
        [
            "name",
            "department",
            "joining_date",
            "exit_date",
            "tenure",
            "status",
            "tenure_category"
        ]
    ].round({"tenure": 2})
)

# =====================================
# STEP 10: TOTAL EMPLOYEES
# =====================================

total_employees = len(df)

print("\nTotal Employees:", total_employees)

# =====================================
# STEP 11: AVERAGE TENURE
# =====================================

average_tenure = df["tenure"].mean()

print(
    "Average Tenure:",
    round(average_tenure, 2),
    "Years"
)

# =====================================
# STEP 12: MAXIMUM TENURE
# =====================================

max_tenure = df.loc[df["tenure"].idxmax()]

print("\nMaximum Tenure:")
print("Employee:", max_tenure["name"])
print("Tenure:", round(max_tenure["tenure"], 2), "Years")

# =====================================
# STEP 13: MINIMUM TENURE
# =====================================

min_tenure = df.loc[df["tenure"].idxmin()]

print("\nMinimum Tenure:")
print("Employee:", min_tenure["name"])
print("Tenure:", round(min_tenure["tenure"], 2), "Years")

# =====================================
# STEP 14: DEPARTMENT WISE COUNT
# =====================================

department_count = df["department"].value_counts()

print("\nDepartment Wise Employee Count:")
print(department_count)

# =====================================
# STEP 15: EMPLOYEE STATUS
# =====================================

status_count = df["status"].value_counts()

print("\nEmployee Status Distribution:")
print(status_count)

# =====================================
# STEP 16: TENURE CATEGORY COUNT
# =====================================

category_count = df["tenure_category"].value_counts(
    sort=False
)

print("\nEmployee Tenure Categories:")
print(category_count)

# =====================================
# STEP 17: DEPARTMENT BAR CHART
# =====================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="department",
    hue="department",
    palette="Set2",
    legend=False
)

plt.title("Department Wise Employee Count")
plt.xlabel("Department")
plt.ylabel("Number of Employees")

plt.tight_layout()
plt.savefig("department_chart.png")
plt.show()
plt.close()

# =====================================
# STEP 18: EMPLOYEE STATUS PIE CHART
# =====================================

plt.figure(figsize=(6, 6))

df["status"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    colors=["#2ECC71", "#E74C3C"],
    startangle=90
)

plt.title("Employee Status Distribution")
plt.ylabel("")

plt.tight_layout()
plt.savefig("status_chart.png")
plt.show()
plt.close()

# =====================================
# STEP 19: EMPLOYEE TENURE HISTOGRAM
# =====================================

plt.figure(figsize=(8, 5))

plt.hist(
    df["tenure"].dropna(),
    bins=5,
    color="#3498DB",
    edgecolor="black"
)

plt.title("Employee Tenure Distribution")
plt.xlabel("Tenure in Years")
plt.ylabel("Number of Employees")

plt.tight_layout()
plt.savefig("tenure_chart.png")
plt.show()
plt.close()

# =====================================
# STEP 20: TENURE CATEGORY BAR CHART
# =====================================

plt.figure(figsize=(9, 5))

category_count.plot(
    kind="bar",
    color=["#F39C12", "#3498DB", "#2ECC71", "#9B59B6"],
    edgecolor="black"
)

plt.title("Employee Tenure Categories")
plt.xlabel("Tenure Category")
plt.ylabel("Number of Employees")
plt.xticks(rotation=25, ha="right")

plt.tight_layout()
plt.savefig("tenure_category_chart.png")
plt.show()
plt.close()

# =====================================
# STEP 21: SAVE ANALYSIS REPORT
# =====================================

df.to_csv(
    "employee_tenure_report.csv",
    index=False
)

print("\nAnalysis Completed Successfully!")
print("Charts and Employee Report Saved Successfully!")
