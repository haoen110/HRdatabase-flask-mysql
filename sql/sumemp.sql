SELECT emp.department, MAX( emp.salary) AS MAXIMUM, MIN( emp.salary ) AS MINIMUM, ROUND(AVG(emp.salary),1) AS AVERAGE
FROM employees emp
GROUP BY emp.department
ORDER BY emp.department

SELECT emp.department,COUNT(emp.eid) as EMPLOYEES
FROM employees emp
GROUP BY emp.department
ORDER BY emp.department

SELECT emp.department,sum(emp.salary) as EXPENDITURE
FROM employees emp
GROUP BY emp.department
ORDER BY emp.department