-- =====================================================
-- HR WORKFORCE DATA ANALYSIS
-- SQL Analysis Project
-- Tools: MySQL
-- =====================================================

CREATE DATABASE IF NOT EXISTS hr_workforce_analysis;

USE hr_workforce_analysis;


-- =====================================================
-- 1. CREATE TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100),
    cost_center VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS job_roles (
    role_id INT PRIMARY KEY,
    job_position VARCHAR(150),
    base_salary_benchmark DECIMAL(12,2)
);


CREATE TABLE IF NOT EXISTS emp_info (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(150),
    date_of_birth DATE,
    gender VARCHAR(50),
    marital_status VARCHAR(50),
    qualification VARCHAR(100),
    location VARCHAR(100),
    hire_date DATE,
    active_status VARCHAR(50),
    department_id INT,
    role_id INT
);


CREATE TABLE IF NOT EXISTS emp_salaries (
    employee_id INT,
    basic_salary DECIMAL(12,2),
    pf DECIMAL(12,2),
    esi DECIMAL(12,2),
    performance_rating DECIMAL(5,2),
    performance_bonus DECIMAL(12,2),
    gross_salary DECIMAL(12,2),
    net_salary DECIMAL(12,2)
);


-- =====================================================
-- 2. BASIC WORKFORCE ANALYSIS
-- =====================================================

-- Total Employees
SELECT COUNT(*) AS total_employees
FROM emp_info;


-- Active Employees
SELECT COUNT(*) AS active_employees
FROM emp_info
WHERE LOWER(active_status) = 'active';


-- Active vs Inactive Employees
SELECT
    active_status,
    COUNT(*) AS employee_count
FROM emp_info
GROUP BY active_status;


-- Employees by Gender
SELECT
    gender,
    COUNT(*) AS employee_count
FROM emp_info
GROUP BY gender
ORDER BY employee_count DESC;


-- Employees by Location
SELECT
    location,
    COUNT(*) AS employee_count
FROM emp_info
GROUP BY location
ORDER BY employee_count DESC;


-- Employees by Qualification
SELECT
    qualification,
    COUNT(*) AS employee_count
FROM emp_info
GROUP BY qualification
ORDER BY employee_count DESC;


-- Employees by Marital Status
SELECT
    marital_status,
    COUNT(*) AS employee_count
FROM emp_info
GROUP BY marital_status
ORDER BY employee_count DESC;


-- =====================================================
-- 3. DEPARTMENT ANALYSIS
-- =====================================================

-- Employees by Department
SELECT
    d.department_name,
    COUNT(e.employee_id) AS employee_count
FROM emp_info e
JOIN department d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY employee_count DESC;


-- Average Salary by Department
SELECT
    d.department_name,
    ROUND(AVG(s.basic_salary), 2) AS average_basic_salary
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN department d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_basic_salary DESC;


-- Total Payroll by Department
SELECT
    d.department_name,
    ROUND(SUM(s.gross_salary), 2) AS total_payroll
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN department d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_payroll DESC;


-- Average Performance by Department
SELECT
    d.department_name,
    ROUND(AVG(s.performance_rating), 2) AS average_performance_rating
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN department d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_performance_rating DESC;


-- Performance Bonus by Department
SELECT
    d.department_name,
    ROUND(SUM(s.performance_bonus), 2) AS total_performance_bonus
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN department d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_performance_bonus DESC;


-- =====================================================
-- 4. JOB ROLE ANALYSIS
-- =====================================================

-- Employees by Job Role
SELECT
    r.job_position,
    COUNT(e.employee_id) AS employee_count
FROM emp_info e
JOIN job_roles r
    ON e.role_id = r.role_id
GROUP BY r.job_position
ORDER BY employee_count DESC;


-- Average Salary by Job Role
SELECT
    r.job_position,
    ROUND(AVG(s.basic_salary), 2) AS average_salary
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN job_roles r
    ON e.role_id = r.role_id
GROUP BY r.job_position
ORDER BY average_salary DESC;


-- Salary Benchmark by Job Role
SELECT
    job_position,
    base_salary_benchmark
FROM job_roles
ORDER BY base_salary_benchmark DESC;


-- Performance by Job Role
SELECT
    r.job_position,
    ROUND(AVG(s.performance_rating), 2) AS average_performance
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN job_roles r
    ON e.role_id = r.role_id
GROUP BY r.job_position
ORDER BY average_performance DESC;


-- =====================================================
-- 5. SALARY & COMPENSATION ANALYSIS
-- =====================================================

-- Average Basic Salary
SELECT
    ROUND(AVG(basic_salary), 2) AS average_basic_salary
FROM emp_salaries;


-- Average Gross Salary
SELECT
    ROUND(AVG(gross_salary), 2) AS average_gross_salary
FROM emp_salaries;


-- Average Net Salary
SELECT
    ROUND(AVG(net_salary), 2) AS average_net_salary
FROM emp_salaries;


-- Total Payroll
SELECT
    ROUND(SUM(gross_salary), 2) AS total_payroll
FROM emp_salaries;


-- Total Net Salary
SELECT
    ROUND(SUM(net_salary), 2) AS total_net_salary
FROM emp_salaries;


-- Total Performance Bonus
SELECT
    ROUND(SUM(performance_bonus), 2) AS total_performance_bonus
FROM emp_salaries;


-- Average Performance Bonus
SELECT
    ROUND(AVG(performance_bonus), 2) AS average_performance_bonus
FROM emp_salaries;


-- =====================================================
-- 6. TOP PAID EMPLOYEES
-- =====================================================

SELECT
    e.employee_id,
    e.employee_name,
    s.basic_salary,
    s.gross_salary,
    s.net_salary
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
ORDER BY s.gross_salary DESC
LIMIT 10;


-- =====================================================
-- 7. PERFORMANCE ANALYSIS
-- =====================================================

-- Performance Rating Distribution
SELECT
    performance_rating,
    COUNT(*) AS employee_count
FROM emp_salaries
GROUP BY performance_rating
ORDER BY performance_rating;


-- Average Performance Rating
SELECT
    ROUND(AVG(performance_rating), 2) AS average_performance_rating
FROM emp_salaries;


-- Average Bonus by Performance Rating
SELECT
    performance_rating,
    ROUND(AVG(performance_bonus), 2) AS average_bonus
FROM emp_salaries
GROUP BY performance_rating
ORDER BY performance_rating;


-- Highest Performance Employees
SELECT
    e.employee_id,
    e.employee_name,
    s.performance_rating,
    s.performance_bonus
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
ORDER BY s.performance_rating DESC
LIMIT 10;


-- =====================================================
-- 8. DEDUCTION ANALYSIS
-- =====================================================

-- Total PF and ESI
SELECT
    ROUND(SUM(pf), 2) AS total_pf,
    ROUND(SUM(esi), 2) AS total_esi
FROM emp_salaries;


-- Average Total Deduction
SELECT
    ROUND(AVG(pf + esi), 2) AS average_total_deduction
FROM emp_salaries;


-- Department-wise Total Deductions
SELECT
    d.department_name,
    ROUND(SUM(s.pf + s.esi), 2) AS total_deductions
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN department d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_deductions DESC;


-- =====================================================
-- 9. HIRING TREND ANALYSIS
-- =====================================================

SELECT
    YEAR(hire_date) AS hire_year,
    COUNT(*) AS employees_hired
FROM emp_info
GROUP BY YEAR(hire_date)
ORDER BY hire_year;


-- =====================================================
-- 10. SALARY VS JOB ROLE BENCHMARK
-- =====================================================

SELECT
    e.employee_id,
    e.employee_name,
    r.job_position,
    s.basic_salary,
    r.base_salary_benchmark,
    ROUND(
        s.basic_salary - r.base_salary_benchmark,
        2
    ) AS salary_difference
FROM emp_info e
JOIN emp_salaries s
    ON e.employee_id = s.employee_id
JOIN job_roles r
    ON e.role_id = r.role_id
ORDER BY salary_difference DESC;


-- =====================================================
-- 11. CONSOLIDATED HR ANALYSIS
-- =====================================================

SELECT
    e.employee_id,
    e.employee_name,
    e.gender,
    e.location,
    e.active_status,
    e.hire_date,
    d.department_name,
    r.job_position,
    s.basic_salary,
    s.gross_salary,
    s.net_salary,
    s.performance_rating,
    s.performance_bonus
FROM emp_info e
LEFT JOIN emp_salaries s
    ON e.employee_id = s.employee_id
LEFT JOIN department d
    ON e.department_id = d.department_id
LEFT JOIN job_roles r
    ON e.role_id = r.role_id;
