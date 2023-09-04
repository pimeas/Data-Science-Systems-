# Question 1
select employees.gender, count(*) 
	from employees 
    where employees.gender in ('M', 'F') 
    group by 1 
    order by count(*) desc;

# Question 2
select round(avg(salaries.salary), 2) as average_salary, titles.title 
	from salaries join titles 
	where titles.emp_no = salaries.emp_no
    group by titles.title
    order by average_salary desc;

# Question 3 
select employees.first_name, employees.last_name, count(dept_emp.emp_no) as dep_worked
	from employees natural join dept_emp 
    where employees.emp_no = dept_emp.emp_no
    group by dept_emp.emp_no 
    having dep_worked >= 2 
    order by dep_worked;

# Question 4
select employees.first_name, employees.last_name, salaries.salary
	from employees natural join salaries 
    order by salaries.salary desc 
    limit 1;

# Question 5
select employees.first_name, employees.last_name, salaries.salary
	from employees natural join salaries 
    order by salaries.salary desc
    limit 1, 1;

# Question 6
select month(hire_date) as hire_month, count(month(hire_date)) as count_hire_month
	from employees
    group by hire_month
    order by count_hire_month 
    desc limit 1;

# Question 7
select departments.dept_name, min(floor(datediff(employees.hire_date, employees.birth_date) /365)) as age_of_youngest
	from departments join dept_emp 
    on dept_emp.dept_no = departments.dept_no
	join employees on dept_emp.emp_no = employees.emp_no
    group by departments.dept_name;

# Question 8
select employees.first_name, departments.dept_name 
	from employees join dept_emp
	on dept_emp.emp_no = employees.emp_no
    join departments
    on dept_emp.dept_no = departments.dept_no
    where locate('a', employees.first_name) = 0
    and locate('e', employees.first_name) = 0
    and locate('i', employees.first_name) = 0
    and locate('o', employees.first_name) = 0
    and locate('u', employees.first_name) = 0;
