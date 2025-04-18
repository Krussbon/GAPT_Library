SELECT 
    e1.serial_no,
    e1.salary AS old_salary,
    e2.salary AS new_salary,
    e1.enddated AS change_date
FROM 
    temporal.employee e1
JOIN 
    temporal.employee e2
ON 
    e1.serial_no = e2.serial_no
    AND e1.enddated = e2.enddated
ORDER BY 
    e1.serial_no, e1.enddated;
