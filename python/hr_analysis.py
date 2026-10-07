# Step 1: Import Required Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Optional display settings
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

##  Load the Datasets
# Employee information
emp_info = pd.read_csv(
    "data/raw/emp_info.csv"
)

# Salary information
emp_salaries = pd.read_csv(
    "data/raw/emp_salaries.csv"
)

# Department information
department = pd.read_csv(
    "data/raw/department.csv"
)

# Job role information
job_roles = pd.read_csv(
    "data/raw/job_roles.csv"
)

# Display first five records
emp_info.head()
emp_salaries.head()
department.head()
job_roles.head()

# Check shapes
print(emp_info.shape)
print(emp_salaries.shape)
print(department.shape)
print(job_roles.shape)

# Check column names
print(emp_info.columns)
print(emp_salaries.columns)
print(department.columns)
print(job_roles.columns)

## Understand the Datasets

# Display data types
emp_info.dtypes
emp_salaries.dtypes

# Display dataset information
emp_info.info()
emp_salaries.info()
department.info()
job_roles.info()

# Statistical summary
emp_info.describe(include="all")
emp_salaries.describe(include="all")

# Unique values
emp_info.nunique()
emp_salaries.nunique()

# Duplicate records
emp_info.duplicated().sum()
emp_salaries.duplicated().sum()

# Unique departments
department["department_name"].unique()

# Unique job roles
job_roles["job_position"].unique()

##  Missing Values

# Check missing values
emp_info.isnull().sum()
emp_salaries.isnull().sum()
department.isnull().sum()
job_roles.isnull().sum()

# Missing-value percentage
missing_percentage = (
    emp_info.isnull().sum() / len(emp_info)
) * 100

missing_percentage.sort_values(
    ascending=False
)

# Missing-value summary
missing_summary = pd.DataFrame({
    "Missing Values": emp_info.isnull().sum(),
    "Missing Percentage": missing_percentage
})

missing_summary.sort_values(
    by="Missing Percentage",
    ascending=False
)

# Salary missing percentage
salary_missing_percentage = (
    emp_salaries.isnull().sum() /
    len(emp_salaries)
) * 100

# Visualize missing values
plt.figure(figsize=(12, 6))

sns.heatmap(
    emp_info.isnull(),
    cbar=False
)

plt.title("Missing Values in Employee Dataset")
plt.show()

##  Data Cleaning

# Standardize column names

for data in [
    emp_info,
    emp_salaries,
    department,
    job_roles
]:

    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )


# Convert date columns

emp_info["date_of_birth"] = pd.to_datetime(
    emp_info["date_of_birth"],
    errors="coerce"
)

emp_info["hire_date"] = pd.to_datetime(
    emp_info["hire_date"],
    errors="coerce"
)


# Remove duplicate records

emp_info = emp_info.drop_duplicates()
emp_salaries = emp_salaries.drop_duplicates()
department = department.drop_duplicates()
job_roles = job_roles.drop_duplicates()


# Check duplicate employee IDs

emp_info["employee_id"].duplicated().sum()

## Convert Numeric Columns
# Step 6: Convert Numeric Columns

salary_columns = [
    "basic_salary",
    "pf",
    "esi",
    "performance_rating",
    "performance_bonus",
    "gross_salary",
    "net_salary"
]

for column in salary_columns:
    emp_salaries[column] = pd.to_numeric(
        emp_salaries[column],
        errors="coerce"
    )

job_roles["base_salary_benchmark"] = pd.to_numeric(
    job_roles["base_salary_benchmark"],
    errors="coerce"
)

## Data Validation

######## Step 7: Data Validation

# 7.1 Check Invalid Salaries

emp_salaries[
    (emp_salaries["basic_salary"] < 0) |
    (emp_salaries["gross_salary"] < 0) |
    (emp_salaries["net_salary"] < 0)
]


# 7.2 Check Invalid Deductions

emp_salaries[
    (emp_salaries["pf"] < 0) |
    (emp_salaries["esi"] < 0)
]


# 7.3 Check Invalid Performance Ratings

emp_salaries[
    emp_salaries["performance_rating"] < 0
]


# 7.4 Check Employee IDs

emp_info["employee_id"].isnull().sum()

emp_salaries["employee_id"].isnull().sum()


# 7.5 Check Department IDs

department["department_id"].isnull().sum()


# 7.6 Check Role IDs

job_roles["role_id"].isnull().sum()


######## Step 8: Integrate the Relational Datasets

# Employee + Salary

hr_data = emp_info.merge(
    emp_salaries,
    on="employee_id",
    how="left"
)


# Join Department Information

hr_data = hr_data.merge(
    department,
    on="department_id",
    how="left"
)


# Join Job Role Information

hr_data = hr_data.merge(
    job_roles,
    on="role_id",
    how="left"
)


# Check Final Dataset

hr_data.head()

hr_data.shape

hr_data.info()


######### Step 9: Feature Engineering

# 9.1 Extract Hire Year

hr_data["hire_year"] = (
    hr_data["hire_date"].dt.year
)


# 9.2 Extract Hire Month

hr_data["hire_month"] = (
    hr_data["hire_date"].dt.month
)


# 9.3 Extract Hire Month Name

hr_data["hire_month_name"] = (
    hr_data["hire_date"].dt.month_name()
)


# 9.4 Extract Hire Quarter

hr_data["hire_quarter"] = (
    hr_data["hire_date"].dt.quarter
)


# 9.5 Calculate Salary After Deductions

hr_data["calculated_net_salary"] = (
    hr_data["gross_salary"]
    - hr_data["pf"]
    - hr_data["esi"]
)


# 9.6 Calculate Total Deductions

hr_data["total_deductions"] = (
    hr_data["pf"]
    + hr_data["esi"]
)


# 9.7 Calculate Salary Difference from Benchmark

hr_data["salary_vs_benchmark"] = (
    hr_data["basic_salary"]
    - hr_data["base_salary_benchmark"]
)


# 9.8 Calculate Total Compensation

hr_data["total_compensation"] = (
    hr_data["gross_salary"]
    + hr_data["performance_bonus"]
)


##########3 Step 10: Basic Dataset Analysis

# 10.1 Total Employees

total_employees = (
    hr_data["employee_id"].nunique()
)

total_employees


# 10.2 Total Departments

total_departments = (
    hr_data["department_name"].nunique()
)

total_departments


# 10.3 Total Job Roles

total_job_roles = (
    hr_data["job_position"].nunique()
)

total_job_roles


# 10.4 Total Locations

total_locations = (
    hr_data["location"].nunique()
)

total_locations


# 10.5 Active Employees

active_employees = hr_data[
    hr_data["active_status"]
    .str.lower() == "active"
]

active_employees_count = (
    active_employees["employee_id"]
    .nunique()
)

active_employees_count

######### Step 11: Workforce Analysis

# 11.1 Employees by Department

employees_by_department = (
    hr_data["department_name"]
    .value_counts()
    .reset_index()
)

employees_by_department.columns = [
    "department",
    "employee_count"
]

employees_by_department


# 11.2 Employees by Location

employees_by_location = (
    hr_data["location"]
    .value_counts()
    .reset_index()
)

employees_by_location.columns = [
    "location",
    "employee_count"
]

employees_by_location


# 11.3 Employees by Gender

gender_distribution = (
    hr_data["gender"]
    .value_counts()
    .reset_index()
)

gender_distribution.columns = [
    "gender",
    "employee_count"
]

gender_distribution


# 11.4 Employees by Qualification

qualification_distribution = (
    hr_data["qualification"]
    .value_counts()
    .reset_index()
)

qualification_distribution.columns = [
    "qualification",
    "employee_count"
]

qualification_distribution


# 11.5 Employees by Marital Status

marital_distribution = (
    hr_data["marital_status"]
    .value_counts()
    .reset_index()
)

marital_distribution.columns = [
    "marital_status",
    "employee_count"
]

marital_distribution


######### Step 12: Active and Inactive Employee Analysis

# 12.1 Active Status Distribution

status_distribution = (
    hr_data["active_status"]
    .value_counts()
    .reset_index()
)

status_distribution.columns = [
    "status",
    "employee_count"
]

status_distribution


# 12.2 Active Employee Percentage

active_percentage = (
    active_employees_count /
    total_employees
) * 100

active_percentage


# 12.3 Active Employees by Department

active_by_department = (
    hr_data[
        hr_data["active_status"]
        .str.lower() == "active"
    ]
    .groupby("department_name")
    ["employee_id"]
    .nunique()
    .reset_index(
        name="active_employees"
    )
)

active_by_department

########## Step 13: Hiring Trend Analysis

# 13.1 Employees Hired by Year

hiring_trend = (
    hr_data.groupby("hire_year")
    ["employee_id"]
    .nunique()
    .reset_index(
        name="employees_hired"
    )
)

hiring_trend


# 13.2 Hiring Trend Visualization

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=hiring_trend,
    x="hire_year",
    y="employees_hired",
    marker="o"
)

plt.title("Employee Hiring Trend")
plt.xlabel("Hire Year")
plt.ylabel("Employees Hired")

plt.show()

######### Step 14: Department Analysis

# 14.1 Department Employee Count

department_employee_count = (
    hr_data.groupby("department_name")
    ["employee_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
)

department_employee_count


# 14.2 Average Salary by Department

department_salary = (
    hr_data.groupby("department_name")
    ["basic_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

department_salary


# 14.3 Average Net Salary by Department

department_net_salary = (
    hr_data.groupby("department_name")
    ["net_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

department_net_salary


# 14.4 Total Payroll by Department

department_payroll = (
    hr_data.groupby("department_name")
    ["gross_salary"]
    .sum()
    .sort_values(
        ascending=False
    )
)

department_payroll


# 14.5 Performance by Department

department_performance = (
    hr_data.groupby("department_name")
    ["performance_rating"]
    .mean()
    .sort_values(
        ascending=False
    )
)

department_performance

######## Step 15: Department Salary Visualization

department_salary_df = (
    department_salary
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=department_salary_df,
    x="basic_salary",
    y="department_name"
)

plt.title(
    "Average Basic Salary by Department"
)

plt.xlabel("Average Basic Salary")
plt.ylabel("Department")

plt.show()


######### Step 16: Job Role Analysis

# 16.1 Employees by Job Role

role_employee_count = (
    hr_data["job_position"]
    .value_counts()
    .reset_index()
)

role_employee_count.columns = [
    "job_position",
    "employee_count"
]

role_employee_count


# 16.2 Average Salary by Job Role

role_salary = (
    hr_data.groupby("job_position")
    ["basic_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

role_salary


# 16.3 Salary Benchmark by Job Role

role_benchmark = (
    hr_data.groupby("job_position")
    ["base_salary_benchmark"]
    .mean()
    .sort_values(
        ascending=False
    )
)

role_benchmark


# 16.4 Performance by Job Role

role_performance = (
    hr_data.groupby("job_position")
    ["performance_rating"]
    .mean()
    .sort_values(
        ascending=False
    )
)

role_performance

######## Step 17: Salary Analysis

# 17.1 Average Basic Salary

average_basic_salary = (
    hr_data["basic_salary"]
    .mean()
)

average_basic_salary


# 17.2 Average Gross Salary

average_gross_salary = (
    hr_data["gross_salary"]
    .mean()
)

average_gross_salary


# 17.3 Average Net Salary

average_net_salary = (
    hr_data["net_salary"]
    .mean()
)

average_net_salary


# 17.4 Total Payroll

total_payroll = (
    hr_data["gross_salary"]
    .sum()
)

total_payroll


# 17.5 Salary Distribution

plt.figure(figsize=(10, 6))

sns.histplot(
    data=hr_data,
    x="basic_salary",
    kde=True
)

plt.title("Basic Salary Distribution")
plt.xlabel("Basic Salary")
plt.ylabel("Employee Count")

plt.show()

########3 Step 18: Salary Benchmark Analysis

# 18.1 Salary Difference from Benchmark

hr_data["salary_difference"] = (
    hr_data["basic_salary"]
    - hr_data["base_salary_benchmark"]
)

hr_data[
    [
        "employee_id",
        "job_position",
        "basic_salary",
        "base_salary_benchmark",
        "salary_difference"
    ]
].head()


# 18.2 Employees Below Benchmark

below_benchmark = hr_data[
    hr_data["salary_difference"] < 0
]

below_benchmark[
    [
        "employee_id",
        "job_position",
        "basic_salary",
        "base_salary_benchmark",
        "salary_difference"
    ]
]


# 18.3 Employees Above Benchmark

above_benchmark = hr_data[
    hr_data["salary_difference"] > 0
]

above_benchmark[
    [
        "employee_id",
        "job_position",
        "basic_salary",
        "base_salary_benchmark",
        "salary_difference"
    ]
]


# 18.4 Average Salary Difference by Job Role

benchmark_by_role = (
    hr_data.groupby("job_position")
    ["salary_difference"]
    .mean()
    .sort_values(
        ascending=False
    )
)

benchmark_by_role

########### Step 19: Compensation Analysis

# 19.1 Total Performance Bonus

total_bonus = (
    hr_data["performance_bonus"]
    .sum()
)

total_bonus


# 19.2 Average Performance Bonus

average_bonus = (
    hr_data["performance_bonus"]
    .mean()
)

average_bonus


# 19.3 Total PF

total_pf = (
    hr_data["pf"]
    .sum()
)

total_pf


# 19.4 Total ESI

total_esi = (
    hr_data["esi"]
    .sum()
)

total_esi


# 19.5 Total Deductions

total_deductions = (
    hr_data["total_deductions"]
    .sum()
)

total_deductions

########### Step 20: Performance Analysis

# 20.1 Performance Rating Distribution

performance_distribution = (
    hr_data["performance_rating"]
    .value_counts()
    .sort_index()
)

performance_distribution


# 20.2 Average Performance Rating

average_performance = (
    hr_data["performance_rating"]
    .mean()
)

average_performance


# 20.3 Performance by Department

performance_by_department = (
    hr_data.groupby("department_name")
    ["performance_rating"]
    .mean()
    .sort_values(
        ascending=False
    )
)

performance_by_department


# 20.4 Performance by Job Role

performance_by_role = (
    hr_data.groupby("job_position")
    ["performance_rating"]
    .mean()
    .sort_values(
        ascending=False
    )
)

performance_by_role

######## Step 21: Performance Bonus Analysis

# 21.1 Average Bonus by Performance Rating

bonus_by_rating = (
    hr_data.groupby("performance_rating")
    ["performance_bonus"]
    .mean()
)

bonus_by_rating


# 21.2 Total Bonus by Department

bonus_by_department = (
    hr_data.groupby("department_name")
    ["performance_bonus"]
    .sum()
    .sort_values(
        ascending=False
    )
)

bonus_by_department


# 21.3 Performance Rating vs Bonus

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=hr_data,
    x="performance_rating",
    y="performance_bonus"
)

plt.title(
    "Performance Rating vs Performance Bonus"
)

plt.xlabel("Performance Rating")
plt.ylabel("Performance Bonus")

plt.show()

########3# Step 22: Employee Demographic Analysis

# 22.1 Gender Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=hr_data,
    x="gender"
)

plt.title(
    "Employee Distribution by Gender"
)

plt.xlabel("Gender")
plt.ylabel("Employee Count")

plt.show()


# 22.2 Qualification Distribution

plt.figure(figsize=(10, 6))

sns.countplot(
    data=hr_data,
    y="qualification"
)

plt.title(
    "Employee Distribution by Qualification"
)

plt.xlabel("Employee Count")
plt.ylabel("Qualification")

plt.show()


# 22.3 Marital Status Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=hr_data,
    x="marital_status"
)

plt.title(
    "Employee Distribution by Marital Status"
)

plt.xlabel("Marital Status")
plt.ylabel("Employee Count")

plt.show()

########## Step 23: Location Analysis

# 23.1 Employees by Location

location_analysis = (
    hr_data.groupby("location")
    ["employee_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
)

location_analysis


# 23.2 Average Salary by Location

location_salary = (
    hr_data.groupby("location")
    ["basic_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

location_salary


# 23.3 Average Performance by Location

location_performance = (
    hr_data.groupby("location")
    ["performance_rating"]
    .mean()
    .sort_values(
        ascending=False
    )
)

location_performance
# Step 24: Statistical Analysis

# 24.1 Salary Statistics

salary_columns = [
    "basic_salary",
    "gross_salary",
    "net_salary",
    "performance_bonus",
    "total_deductions"
]

hr_data[salary_columns].describe()


# 24.2 Correlation Analysis

numeric_columns = [
    "basic_salary",
    "gross_salary",
    "net_salary",
    "pf",
    "esi",
    "performance_rating",
    "performance_bonus",
    "base_salary_benchmark",
    "total_deductions"
]

correlation_matrix = (
    hr_data[numeric_columns].corr()
)

correlation_matrix


# 24.3 Correlation Heatmap

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm"
)

plt.title(
    "Correlation Matrix of HR Workforce Metrics"
)

plt.show()



########### Step 25: Additional Workforce Insights

# 25.1 Employees by Hire Year and Department

hiring_department = (
    hr_data.groupby(
        ["hire_year", "department_name"]
    )["employee_id"]
    .nunique()
    .reset_index(
        name="employee_count"
    )
)

hiring_department


# 25.2 Employees by Hire Year and Gender

hiring_gender = (
    hr_data.groupby(
        ["hire_year", "gender"]
    )["employee_id"]
    .nunique()
    .reset_index(
        name="employee_count"
    )
)

hiring_gender


# 25.3 Hiring Trend by Month

hiring_month = (
    hr_data.groupby("hire_month")
    ["employee_id"]
    .nunique()
    .reset_index(
        name="employee_count"
    )
)

hiring_month


# 25.4 Hiring Trend Visualization

plt.figure(figsize=(12, 6))

sns.barplot(
    data=hiring_month,
    x="hire_month",
    y="employee_count"
)

plt.title(
    "Employee Hiring Trend by Month"
)

plt.xlabel("Hire Month")
plt.ylabel("Employee Count")

plt.show()


######### Step 26: Top Paid Employees

# 26.1 Top 10 Employees by Basic Salary

top_paid_employees = (
    hr_data[
        [
            "employee_id",
            "employee_name",
            "department_name",
            "job_position",
            "basic_salary",
            "gross_salary",
            "net_salary"
        ]
    ]
    .sort_values(
        by="basic_salary",
        ascending=False
    )
    .head(10)
)

top_paid_employees


# 26.2 Top 10 Employees by Gross Salary

top_gross_salary = (
    hr_data[
        [
            "employee_id",
            "employee_name",
            "department_name",
            "job_position",
            "gross_salary"
        ]
    ]
    .sort_values(
        by="gross_salary",
        ascending=False
    )
    .head(10)
)

top_gross_salary


# 26.3 Top 10 Employees by Performance Bonus

top_bonus_employees = (
    hr_data[
        [
            "employee_id",
            "employee_name",
            "department_name",
            "job_position",
            "performance_rating",
            "performance_bonus"
        ]
    ]
    .sort_values(
        by="performance_bonus",
        ascending=False
    )
    .head(10)
)

top_bonus_employees


# Step 27: Salary and Performance Relationship

# 27.1 Average Salary by Performance Rating

salary_by_performance = (
    hr_data.groupby("performance_rating")
    ["basic_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

salary_by_performance


# 27.2 Average Gross Salary by Performance Rating

gross_salary_by_performance = (
    hr_data.groupby("performance_rating")
    ["gross_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

gross_salary_by_performance


####### 27.3 Average Net Salary by Performance Rating

net_salary_by_performance = (
    hr_data.groupby("performance_rating")
    ["net_salary"]
    .mean()
    .sort_values(
        ascending=False
    )
)

net_salary_by_performance


####### 27.4 Salary vs Performance Visualization

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=hr_data,
    x="performance_rating",
    y="basic_salary"
)

plt.title(
    "Basic Salary by Performance Rating"
)

plt.xlabel("Performance Rating")
plt.ylabel("Basic Salary")

plt.show()

######### Step 28: Employee Salary Distribution by Department

plt.figure(figsize=(14, 7))

sns.boxplot(
    data=hr_data,
    x="department_name",
    y="basic_salary"
)

plt.title(
    "Salary Distribution by Department"
)

plt.xlabel("Department")
plt.ylabel("Basic Salary")

plt.xticks(
    rotation=45
)

plt.show()

####### Step 29: Salary Distribution by Job Role

plt.figure(figsize=(14, 7))

sns.boxplot(
    data=hr_data,
    x="job_position",
    y="basic_salary"
)

plt.title(
    "Salary Distribution by Job Role"
)

plt.xlabel("Job Position")
plt.ylabel("Basic Salary")

plt.xticks(
    rotation=45
)

plt.show()

# Step 30: Employee Age Analysis

# 30.1 Calculate Employee Age

current_date = pd.Timestamp.today()

hr_data["age"] = (
    (
        current_date
        - hr_data["date_of_birth"]
    ).dt.days / 365.25
)


# Convert Age into Years

hr_data["age"] = (
    hr_data["age"]
    .round()
    .astype("Int64")
)

hr_data[
    [
        "employee_id",
        "employee_name",
        "date_of_birth",
        "age"
    ]
].head()


# 30.2 Average Employee Age

average_age = (
    hr_data["age"]
    .mean()
)

average_age


# 30.3 Minimum Employee Age

minimum_age = (
    hr_data["age"]
    .min()
)

minimum_age


# 30.4 Maximum Employee Age

maximum_age = (
    hr_data["age"]
    .max()
)

maximum_age


# 30.5 Age Distribution

plt.figure(figsize=(10, 6))

sns.histplot(
    data=hr_data,
    x="age",
    kde=True
)

plt.title(
    "Employee Age Distribution"
)

plt.xlabel("Age")
plt.ylabel("Employee Count")

plt.show()
