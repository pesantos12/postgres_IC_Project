/*
Questão 1 - Selecione todos os registros da tabela de cargos ("jobs")
*/

/*
Questão 1 - Selecione todos os registros da tabela de cargos
*/

/*
Questão 1 - Selecione todos os registros da tabela de cargos

Dica: Tabela Cargos = Tabela "Jobs"
*/

SELECT * FROM Jobs;
-- 19 rows





/*
Questão 2 - Exiba todos os nomes dos países cadastrados
*/

/*
Questão 2 - Exiba todos os nome dos países cadastrados

Tab -> Countries
*/

/*
Questão 2 - Exiba todos os nome dos países ("country_name") cadastrados
*/

SELECT country_name FROM countries;
-- 25 rows





/*
Questão 3 - Liste os títulos de trabalho (job_title) e seus respectivos salários máximos da tabela jobs.
*/

/*
Questão 3 - Liste os títulos de trabalho e seus respectivos salários máximos.
*/

/*
Questão 3 - Liste os títulos de trabalho e seus respectivos salários máximos.

Dica: Conteúdo na tabela Jobs.
*/


SELECT job_title, max_salary FROM jobs;
-- 19 rows




/*
Questão 4 - Encontre os dados do Funcionário com o id 177
*/

/*
Questão 4 - Encontre os dados do Funcionário com o número de identificação (employee_id) 177
*/

/*
Questão 4 - Encontre os dados do Funcionário com o número de identificação 177

Dica: Funcionário = Employee
*/

SELECT * FROM employees WHERE employee_id = 177;




/*
Questão 5 - Liste os funcionários com salário superior a 7 mil
*/

/*
Questão 5 - Liste os funcionários com salário (salary) superior a 7 mil
*/

/*
Questão 5 - Liste os funcionários com salário (salary) superior a 7 mil

Dica: Funcionário = Employee
*/

SELECT * FROM employees WHERE salary > 7000;