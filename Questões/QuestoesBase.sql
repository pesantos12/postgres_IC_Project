INSERT INTO questions (question_text, correct_query) VALUES
-- 1. Seleção básica de todos os registros de uma tabela
('Selecione todos os registros da tabela de cargos.', 
 'SELECT * FROM jobs;'
),

-- 2. Seleção de uma coluna específica
('Exiba os nomes de todos os países cadastrados.', 
 'SELECT country_name FROM countries;'
),

-- 3. Ordenação simples por uma coluna
('Liste os funcionários ordenados por salário em ordem crescente.', 
 'SELECT * FROM employees ORDER BY salary ASC;'
),

-- 4. Filtro simples com condição de igualdade
('Encontre os dados do funcionário com o ID 101.', 
 'SELECT * FROM employees WHERE employee_id = 101;'
),

-- 5. Filtro com operador lógico
('Liste os funcionários que ganham mais de 5000 e trabalham no departamento 10.', 
 'SELECT * FROM employees WHERE salary > 5000 AND department_id = 10;'
),

-- 6. Seleção com alias para colunas
('Mostre os nomes dos países e utilize o alias "País" para a coluna.', 
 'SELECT country_name AS "País" FROM countries;'
),

-- 7. Filtro utilizando o operador IN
('Liste os departamentos com os IDs 10, 20 e 30.', 
 'SELECT * FROM departments WHERE department_id IN (10, 20, 30);'
),

-- 8. Filtro com intervalo utilizando BETWEEN
('Liste os funcionários que ganham entre 3000 e 8000.', 
 'SELECT * FROM employees WHERE salary BETWEEN 3000 AND 8000;'
),

-- 9. Seleção limitada de resultados
('Exiba os 5 primeiros funcionários cadastrados.', 
 'SELECT * FROM employees LIMIT 5;'
),

-- 10. Filtro com operador LIKE
('Liste os funcionários cujo nome começa com "A".', 
 'SELECT * FROM employees WHERE first_name LIKE ''A%'';'
),

-- 11. Operador lógico básico
('Liste os funcionários que trabalham no departamento 30 ou 50.',
 'SELECT * FROM employees WHERE department_id = 30 OR department_id = 50;'
),

-- 12. Filtro com texto e operador LIKE
('Liste os países cujo nome termina com "a".',
 'SELECT * FROM countries WHERE country_name LIKE ''%a'';'
),

-- 13. Função de agregação simples
('Exiba o número total de funcionários cadastrados.',
 'SELECT COUNT(*) FROM employees;'
),

-- 14. Filtro combinado com função de agregação
('Exiba o número total de funcionários que ganham mais de 3000.',
 'SELECT COUNT(*) FROM employees WHERE salary > 3000;'
),

-- 15. Ordenação descendente
('Liste os cargos ordenados por salário máximo em ordem decrescente.',
 'SELECT * FROM jobs ORDER BY max_salary DESC;'
),

-- 16. Agrupamento básico
('Exiba o número de funcionários por departamento.',
 'SELECT department_id, COUNT(*) FROM employees GROUP BY department_id;'
),

-- 17. Filtro em grupos
('Liste os departamentos que têm mais de 5 funcionários.',
 'SELECT department_id, COUNT(*) FROM employees GROUP BY department_id HAVING COUNT(*) > 5;'
),

-- 18. Uso de alias para tabelas
('Liste o ID e o nome dos funcionários, usando alias "ID" e "Nome".',
 'SELECT employee_id AS "ID", first_name AS "Nome" FROM employees;'
),

-- 19. Filtro de intervalo
('Exiba os funcionários cujos salários estejam entre 4000 e 9000.',
 'SELECT * FROM employees WHERE salary BETWEEN 4000 AND 9000;'
),

-- 20. Join básico
('Liste os nomes dos funcionários e os nomes de seus departamentos.',
 'SELECT e.first_name, d.department_name FROM employees e JOIN departments d ON e.department_id = d.department_id;'
),

-- 21. Subconsulta simples em SELECT
('Exiba o nome dos funcionários cujo salário é maior que a média salarial de todos os funcionários.',
 'SELECT first_name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);'
),

-- 22. Uso de funções de agregação combinadas
('Mostre o menor e o maior salário registrados na tabela de funcionários.',
 'SELECT MIN(salary) AS menor_salario, MAX(salary) AS maior_salario FROM employees;'
),

-- 23. Join com três tabelas
('Liste o nome dos funcionários, o nome de seus departamentos e o nome de suas localidades.',
 'SELECT e.first_name, d.department_name, l.city 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id;'
),

-- 24. Filtro por data com BETWEEN
('Liste os históricos de trabalho registrados entre 01/01/2000 e 31/12/2010.',
 'SELECT * FROM job_history WHERE start_date BETWEEN ''2000-01-01'' AND ''2010-12-31'';'
),

-- 25. Contagem de registros com filtro
('Conte quantos funcionários têm salários superiores a 5000.',
 'SELECT COUNT(*) FROM employees WHERE salary > 5000;'
),

-- 26. Agrupamento com filtro HAVING avançado
('Liste os IDs dos departamentos que possuem média salarial superior a 10000.',
 'SELECT department_id, AVG(salary) 
  FROM employees 
  GROUP BY department_id 
  HAVING AVG(salary) > 10000;'
),

-- 27. Join com filtro específico
('Liste os nomes dos funcionários que trabalham em departamentos localizados em "Seattle".',
 'SELECT e.first_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  WHERE l.city = ''Seattle'';'
),

-- 28. Filtro com subconsulta correlacionada
('Liste os nomes dos funcionários que ganham mais que o salário médio do departamento onde trabalham.',
 'SELECT first_name 
  FROM employees e 
  WHERE salary > (
    SELECT AVG(salary) 
    FROM employees 
    WHERE department_id = e.department_id
  );'
),

-- 29. Ordenação múltipla
('Liste todos os funcionários ordenados pelo ID do departamento em ordem crescente e, dentro de cada departamento, pelo salário em ordem decrescente.',
 'SELECT * FROM employees ORDER BY department_id ASC, salary DESC;'
),

-- 30. Join com alias e filtro composto
('Exiba os nomes dos funcionários e suas localizações, filtrando por departamentos cujo nome começa com "A".',
 'SELECT e.first_name, l.city 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  WHERE d.department_name LIKE ''A%'';'
),

-- 31. Uso de CASE
('Exiba o nome dos funcionários e uma coluna que indica "Alto" se o salário for maior que 8000, ou "Baixo" caso contrário.',
 'SELECT first_name, 
         CASE 
             WHEN salary > 8000 THEN ''Alto''
             ELSE ''Baixo''
         END AS classificacao_salario
  FROM employees;'
),

-- 32. Subconsulta no SELECT com agregação
('Exiba os nomes dos departamentos e o número de funcionários em cada um deles.',
 'SELECT d.department_name, 
         (SELECT COUNT(*) 
          FROM employees e 
          WHERE e.department_id = d.department_id) AS total_funcionarios
  FROM departments d;'
),

-- 33. Joins múltiplos e filtro composto
('Liste os nomes dos funcionários, seus cargos e o departamento onde trabalham, filtrando apenas os funcionários cujo salário é maior que 6000.',
 'SELECT e.first_name, j.job_title, d.department_name 
  FROM employees e 
  JOIN jobs j ON e.job_id = j.job_id 
  JOIN departments d ON e.department_id = d.department_id 
  WHERE e.salary > 6000;'
),

-- 34. Funções de janela (ROW_NUMBER)
('Liste os nomes dos funcionários com um número de linha para cada um, ordenado por salário decrescente.',
 'SELECT first_name, ROW_NUMBER() OVER (ORDER BY salary DESC) AS numero_linha 
  FROM employees;'
),

-- 35. Join com subconsulta correlacionada
('Liste os nomes dos departamentos que possuem pelo menos um funcionário com salário superior a 10000.',
 'SELECT DISTINCT d.department_name 
  FROM departments d 
  WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id 
      AND e.salary > 10000
  );'
),

-- 36. Subconsulta com IN
('Liste os nomes dos funcionários que trabalham nos departamentos localizados na cidade de "New York".',
 'SELECT e.first_name 
  FROM employees e 
  WHERE e.department_id IN (
    SELECT d.department_id 
    FROM departments d 
    JOIN locations l ON d.location_id = l.location_id 
    WHERE l.city = ''New York''
  );'
),

-- 37. Agrupamento com múltiplas funções de agregação
('Para cada departamento, exiba o número total de funcionários e a soma dos salários.',
 'SELECT department_id, 
         COUNT(*) AS total_funcionarios, 
         SUM(salary) AS soma_salarios
  FROM employees 
  GROUP BY department_id;'
),

-- 38. Filtro avançado com LIKE e JOIN
('Liste os nomes dos funcionários cujo nome do departamento contém "Sales".',
 'SELECT e.first_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  WHERE d.department_name LIKE ''%Sales%'';'
),

-- 39. Funções de janela com particionamento
('Liste os nomes dos funcionários, seus salários e a soma dos salários de seus departamentos.',
 'SELECT e.first_name, e.salary, 
         SUM(e.salary) OVER (PARTITION BY e.department_id) AS soma_departamento
  FROM employees e;'
),

-- 40. Joins múltiplos com filtro de texto
('Liste os nomes dos funcionários, os cargos e as cidades onde trabalham, para funcionários cujo cargo termina com "Manager".',
 'SELECT e.first_name, j.job_title, l.city 
  FROM employees e 
  JOIN jobs j ON e.job_id = j.job_id 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  WHERE j.job_title LIKE ''%Manager'';'
),

-- 41. Subconsulta correlacionada com filtro
('Exiba os nomes dos funcionários cujo salário é o maior dentro do departamento onde trabalham.',
 'SELECT first_name 
  FROM employees e1 
  WHERE salary = (
    SELECT MAX(salary) 
    FROM employees e2 
    WHERE e2.department_id = e1.department_id
  );'),

-- 42. Joins múltiplos com COUNT e HAVING
('Liste os departamentos que possuem mais de 3 funcionários.',
 'SELECT d.department_name, COUNT(e.employee_id) AS total_funcionarios 
  FROM departments d 
  JOIN employees e ON d.department_id = e.department_id 
  GROUP BY d.department_name 
  HAVING COUNT(e.employee_id) > 3;'),

-- 43. Filtro com funções de data
('Liste os funcionários que começaram a trabalhar após o ano de 2010.',
 'SELECT first_name 
  FROM employees 
  WHERE hire_date > ''2010-01-01'';'),

-- 44. Função de janela com RANK
('Liste os nomes dos funcionários com seus salários e sua classificação dentro do departamento.',
 'SELECT first_name, salary, 
         RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS classificacao 
  FROM employees;'),

-- 45. Subconsulta com EXISTS
('Liste os nomes dos funcionários que já tiveram histórico de trabalho registrado.',
 'SELECT e.first_name 
  FROM employees e 
  WHERE EXISTS (
    SELECT 1 
    FROM job_history j 
    WHERE j.employee_id = e.employee_id
  );'),

-- 46. Joins avançados com filtros múltiplos
('Exiba os nomes dos funcionários e suas cidades, filtrando apenas os que trabalham em departamentos cujo ID seja maior que 50.',
 'SELECT e.first_name, l.city 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  WHERE d.department_id > 50;'),

-- 47. Uso de UNION
('Liste os nomes de todos os países e cidades registrados no sistema.',
 'SELECT country_name AS nome 
  FROM countries 
  UNION 
  SELECT city AS nome 
  FROM locations;'),

-- 48. Agrupamento avançado com múltiplos níveis
('Para cada localização, exiba o número total de departamentos e o número total de funcionários.',
 'SELECT l.city, 
         COUNT(DISTINCT d.department_id) AS total_departamentos, 
         COUNT(e.employee_id) AS total_funcionarios 
  FROM locations l 
  JOIN departments d ON l.location_id = d.location_id 
  JOIN employees e ON d.department_id = e.department_id 
  GROUP BY l.city;'),

-- 49. Subconsulta avançada em SELECT
('Exiba o nome dos funcionários e a média salarial do departamento onde trabalham.',
 'SELECT e.first_name, 
         (SELECT AVG(salary) 
          FROM employees e2 
          WHERE e2.department_id = e.department_id) AS media_salarial_departamento 
  FROM employees e;'),

-- 50. Função de janela com densidade de classificação
('Liste os nomes dos funcionários, seus salários e sua classificação densidade dentro do departamento.',
 'SELECT first_name, salary, 
         DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS classificacao_densidade 
  FROM employees;'),

-- 51. Subconsulta simples no WHERE
('Exiba os nomes dos funcionários que trabalham no departamento com o maior número de funcionários.',
 'SELECT first_name 
  FROM employees 
  WHERE department_id = (
    SELECT department_id 
    FROM employees 
    GROUP BY department_id 
    ORDER BY COUNT(*) DESC 
    LIMIT 1
  );'),

-- 52. Join simples com alias
('Liste os nomes dos funcionários e o nome do departamento onde trabalham.',
 'SELECT e.first_name, d.department_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id;'),

-- 53. Ordenação com função de agregação
('Exiba os IDs dos departamentos ordenados pela soma dos salários em ordem decrescente.',
 'SELECT department_id 
  FROM employees 
  GROUP BY department_id 
  ORDER BY SUM(salary) DESC;'),

-- 54. Filtro com operador NOT IN
('Liste os nomes dos funcionários que não possuem histórico de trabalho registrado.',
 'SELECT first_name 
  FROM employees 
  WHERE employee_id NOT IN (
    SELECT employee_id 
    FROM job_history
  );'),

-- 55. Join com filtro de texto
('Liste os nomes dos funcionários e os departamentos onde trabalham, considerando apenas os departamentos cujo nome contém "Tech".',
 'SELECT e.first_name, d.department_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  WHERE d.department_name LIKE ''%Tech%'';'),

-- 56. Subconsulta em SELECT
('Exiba os nomes dos funcionários e o número de departamentos diferentes em que já trabalharam.',
 'SELECT e.first_name, 
         (SELECT COUNT(DISTINCT department_id) 
          FROM job_history j 
          WHERE j.employee_id = e.employee_id) AS num_departamentos 
  FROM employees e;'),

-- 57. Filtro com intervalo de datas
('Liste os funcionários que começaram a trabalhar entre 01/01/2005 e 31/12/2015.',
 'SELECT first_name 
  FROM employees 
  WHERE hire_date BETWEEN ''2005-01-01'' AND ''2015-12-31'';'),

-- 58. Agrupamento básico
('Exiba o número total de funcionários por cidade.',
 'SELECT l.city, COUNT(e.employee_id) AS total_funcionarios 
  FROM locations l 
  JOIN departments d ON l.location_id = d.location_id 
  JOIN employees e ON d.department_id = e.department_id 
  GROUP BY l.city;'),

-- 59. Função de agregação com filtro
('Exiba os IDs dos departamentos onde a soma dos salários ultrapassa 20000.',
 'SELECT department_id 
  FROM employees 
  GROUP BY department_id 
  HAVING SUM(salary) > 20000;'),

-- 60. Join com função de janela
('Liste os nomes dos funcionários e a soma cumulativa de seus salários por departamento.',
 'SELECT e.first_name, 
         SUM(e.salary) OVER (PARTITION BY e.department_id ORDER BY e.salary) AS soma_cumulativa 
  FROM employees e;'),

-- 61. Filtro com múltiplas condições
('Liste os nomes dos funcionários que ganham mais de 5000 e trabalham em departamentos localizados em "London".',
 'SELECT e.first_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  WHERE e.salary > 5000 AND l.city = ''London'';'),

-- 62. Subconsulta com comparação
('Exiba os nomes dos funcionários cujo salário é maior que a soma de todos os salários de seus departamentos.',
 'SELECT first_name 
  FROM employees e 
  WHERE salary > (
    SELECT SUM(salary) 
    FROM employees 
    WHERE department_id = e.department_id
  );'),

-- 63. Join com COUNT e filtro no HAVING
('Liste os departamentos que possuem menos de 5 funcionários.',
 'SELECT d.department_name, COUNT(e.employee_id) AS total_funcionarios 
  FROM departments d 
  JOIN employees e ON d.department_id = e.department_id 
  GROUP BY d.department_name 
  HAVING COUNT(e.employee_id) < 5;'),

-- 64. Ordenação complexa
('Liste os nomes dos funcionários ordenados primeiro pela cidade do departamento em ordem alfabética e, dentro de cada cidade, pelo salário em ordem decrescente.',
 'SELECT e.first_name, l.city, e.salary 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  ORDER BY l.city ASC, e.salary DESC;'),

-- 65. Subconsulta correlacionada avançada
('Exiba os nomes dos funcionários cujo salário é maior que o maior salário do departamento 50.',
 'SELECT first_name 
  FROM employees e 
  WHERE salary > (
    SELECT MAX(salary) 
    FROM employees 
    WHERE department_id = 50
  );'),

-- 66. Função de janela com média acumulativa
('Liste os nomes dos funcionários, seus salários e a média acumulativa de seus salários dentro de seus departamentos.',
 'SELECT first_name, salary, 
         AVG(salary) OVER (PARTITION BY department_id ORDER BY salary) AS media_acumulativa 
  FROM employees;'),

-- 67. Agrupamento com múltiplos níveis
('Exiba a soma dos salários de funcionários agrupados por cidade e por departamento.',
 'SELECT l.city, d.department_name, SUM(e.salary) AS soma_salarios 
  FROM locations l 
  JOIN departments d ON l.location_id = d.location_id 
  JOIN employees e ON d.department_id = e.department_id 
  GROUP BY l.city, d.department_name;'),

-- 68. Uso de COALESCE
('Exiba os nomes dos funcionários e seus bônus. Caso o bônus seja nulo, exiba "Sem bônus".',
 'SELECT first_name, COALESCE(commission_pct, ''Sem bônus'') AS bonus 
  FROM employees;'),

-- 69. Subconsulta com DISTINCT
('Exiba os nomes das cidades onde há pelo menos um funcionário trabalhando.',
 'SELECT DISTINCT l.city 
  FROM locations l 
  JOIN departments d ON l.location_id = d.location_id 
  JOIN employees e ON d.department_id = e.department_id;'),

-- 70. Joins múltiplos com filtro complexo
('Liste os nomes dos funcionários, seus cargos e os nomes dos países onde trabalham, considerando apenas países que começam com "U".',
 'SELECT e.first_name, j.job_title, c.country_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  JOIN countries c ON l.country_id = c.country_id 
  WHERE c.country_name LIKE ''U%'';'),

-- 71. Subconsulta em SELECT com soma cumulativa
('Exiba os nomes dos funcionários e a soma dos salários de todos os departamentos onde já trabalharam.',
 'SELECT e.first_name, 
         (SELECT SUM(salary) 
          FROM employees e2 
          WHERE e2.department_id IN (
            SELECT department_id 
            FROM job_history j 
            WHERE j.employee_id = e.employee_id
          )) AS soma_salarios_departamentos
  FROM employees e;'),

-- 72. Joins múltiplos com filtro por intervalo de datas
('Liste os nomes dos funcionários e o histórico de trabalho registrado entre 2015 e 2020.',
 'SELECT e.first_name, j.start_date, j.end_date 
  FROM employees e 
  JOIN job_history j ON e.employee_id = j.employee_id 
  WHERE j.start_date >= ''2015-01-01'' AND j.end_date <= ''2020-12-31'';'),

-- 73. Subconsulta com filtro composto
('Exiba os nomes dos departamentos que possuem funcionários ganhando mais de 8000.',
 'SELECT DISTINCT d.department_name 
  FROM departments d 
  WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id AND e.salary > 8000
  );'),

-- 74. Função de agregação com COUNT e filtro avançado
('Liste os IDs dos departamentos onde mais de 10 funcionários trabalham atualmente.',
 'SELECT department_id, COUNT(*) AS total_funcionarios 
  FROM employees 
  GROUP BY department_id 
  HAVING COUNT(*) > 10;'),

-- 75. Join com cálculo e alias
('Exiba os nomes dos funcionários e a diferença entre o salário atual e o salário máximo permitido para seus cargos.',
 'SELECT e.first_name, 
         (j.max_salary - e.salary) AS diferenca_salarial 
  FROM employees e 
  JOIN jobs j ON e.job_id = j.job_id;'),

-- 76. Ordenação com subconsulta correlacionada
('Liste os funcionários ordenados pela diferença entre seus salários e a média salarial do departamento.',
 'SELECT e.first_name, 
         (e.salary - (SELECT AVG(salary) 
                      FROM employees e2 
                      WHERE e2.department_id = e.department_id)) AS diferenca_media 
  FROM employees e 
  ORDER BY diferenca_media DESC;'),

-- 77. Filtro com operador EXISTS
('Liste os nomes dos funcionários que já tiveram mais de um histórico de trabalho registrado.',
 'SELECT e.first_name 
  FROM employees e 
  WHERE EXISTS (
    SELECT 1 
    FROM job_history j 
    WHERE j.employee_id = e.employee_id 
    GROUP BY j.employee_id 
    HAVING COUNT(*) > 1
  );'),

-- 78. Agrupamento com subconsulta no SELECT
('Exiba os nomes dos departamentos e a média de salários, mas apenas para os departamentos com funcionários atualmente empregados.',
 'SELECT d.department_name, 
         (SELECT AVG(salary) 
          FROM employees e 
          WHERE e.department_id = d.department_id) AS media_salarial 
  FROM departments d 
  WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.department_id
  );'),

-- 79. Filtro avançado com LIKE e função de data
('Liste os nomes dos funcionários que começaram a trabalhar em 2020 e cujo nome começa com "J".',
 'SELECT first_name 
  FROM employees 
  WHERE hire_date BETWEEN ''2020-01-01'' AND ''2020-12-31'' 
    AND first_name LIKE ''J%'';'),

-- 80. Join com UNION
('Liste os nomes das cidades e países registrados no banco de dados.',
 'SELECT l.city AS nome 
  FROM locations l 
  UNION 
  SELECT c.country_name AS nome 
  FROM countries c;')
,

-- 81. Join com filtro de agregação
('Liste os nomes dos funcionários que trabalham em departamentos onde a soma dos salários ultrapassa 50.000.',
 'SELECT e.first_name 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  WHERE e.department_id IN (
    SELECT department_id 
    FROM employees 
    GROUP BY department_id 
    HAVING SUM(salary) > 50000
  );'),

-- 82. Subconsulta com operador ANY
('Exiba os nomes dos funcionários cujo salário é maior que qualquer salário do departamento 10.',
 'SELECT first_name 
  FROM employees 
  WHERE salary > ANY (
    SELECT salary 
    FROM employees 
    WHERE department_id = 10
  );'),

-- 83. Agrupamento com filtro múltiplo
('Liste os departamentos que possuem mais de 5 funcionários e média salarial superior a 8000.',
 'SELECT department_id, AVG(salary) AS media_salarial, COUNT(*) AS total_funcionarios 
  FROM employees 
  GROUP BY department_id 
  HAVING COUNT(*) > 5 AND AVG(salary) > 8000;'),

-- 84. Join com cálculo e ordenação
('Exiba os nomes dos funcionários, os salários e a porcentagem do salário em relação ao salário máximo do cargo.',
 'SELECT e.first_name, e.salary, 
         (e.salary * 100.0 / j.max_salary) AS percentual_salario 
  FROM employees e 
  JOIN jobs j ON e.job_id = j.job_id 
  ORDER BY percentual_salario DESC;'),

-- 85. Filtro com operador NOT EXISTS
('Liste os nomes dos funcionários que nunca trabalharam no departamento 50.',
 'SELECT first_name 
  FROM employees e 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM job_history j 
    WHERE j.employee_id = e.employee_id 
      AND j.department_id = 50
  );'),

-- 86. Subconsulta em SELECT com função de data
('Exiba os nomes dos funcionários e a quantidade de anos que trabalharam, considerando histórico de trabalho.',
 'SELECT e.first_name, 
         (SELECT SUM(EXTRACT(YEAR FROM j.end_date) - EXTRACT(YEAR FROM j.start_date)) 
          FROM job_history j 
          WHERE j.employee_id = e.employee_id) AS anos_trabalhados 
  FROM employees e;'),

-- 87. Agrupamento por função de janela
('Liste os nomes dos funcionários e a soma cumulativa dos salários dentro de cada departamento.',
 'SELECT e.first_name, 
         SUM(e.salary) OVER (PARTITION BY e.department_id ORDER BY e.salary) AS soma_cumulativa 
  FROM employees e;'),

-- 88. Subconsulta com operadores lógicos
('Exiba os nomes dos funcionários que trabalham no departamento com o maior número de funcionários.',
 'SELECT first_name 
  FROM employees 
  WHERE department_id = (
    SELECT department_id 
    FROM employees 
    GROUP BY department_id 
    ORDER BY COUNT(*) DESC 
    LIMIT 1
  );'),

-- 89. Join com COUNT e HAVING
('Liste as cidades onde há mais de 10 funcionários trabalhando atualmente.',
 'SELECT l.city, COUNT(e.employee_id) AS total_funcionarios 
  FROM locations l 
  JOIN departments d ON l.location_id = d.location_id 
  JOIN employees e ON d.department_id = e.department_id 
  GROUP BY l.city 
  HAVING COUNT(e.employee_id) > 10;'),

-- 90. Subconsulta correlacionada avançada
('Exiba os nomes dos funcionários cujo salário é maior que a média salarial de todos os funcionários em departamentos diferentes do deles.',
 'SELECT e.first_name 
  FROM employees e 
  WHERE salary > (
    SELECT AVG(salary) 
    FROM employees e2 
    WHERE e2.department_id <> e.department_id
  );'),

-- 91. Funções de janela com classificação por grupo
('Liste os nomes dos funcionários, os salários e sua posição relativa de salário dentro de seus departamentos.',
 'SELECT e.first_name, e.salary, 
         RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS posicao 
  FROM employees e;'),

-- 92. Subconsulta correlacionada com múltiplos critérios
('Exiba os nomes dos funcionários cujo salário é maior que a soma dos salários de todos os funcionários em departamentos com menos de 5 funcionários.',
 'SELECT first_name 
  FROM employees e 
  WHERE salary > (
    SELECT SUM(salary) 
    FROM employees e2 
    WHERE e2.department_id <> e.department_id 
    GROUP BY e2.department_id 
    HAVING COUNT(e2.employee_id) < 5
  );'),

-- 93. Agrupamento com função HAVING complexa
('Liste os departamentos com soma salarial maior que 100000 e média salarial inferior a 20000.',
 'SELECT department_id, SUM(salary) AS soma_salarial, AVG(salary) AS media_salarial 
  FROM employees 
  GROUP BY department_id 
  HAVING SUM(salary) > 100000 AND AVG(salary) < 20000;'),

-- 94. Subconsulta no SELECT com múltiplas condições
('Exiba os nomes dos funcionários e o total de cargos diferentes que já ocuparam em seu histórico de trabalho.',
 'SELECT e.first_name, 
         (SELECT COUNT(DISTINCT job_id) 
          FROM job_history j 
          WHERE j.employee_id = e.employee_id) AS total_cargos 
  FROM employees e;'),

-- 95. Join múltiplo com subconsulta correlacionada
('Liste os nomes dos funcionários e o nome de suas localidades, considerando apenas os funcionários que trabalham em departamentos com mais de 10 funcionários.',
 'SELECT e.first_name, l.city 
  FROM employees e 
  JOIN departments d ON e.department_id = d.department_id 
  JOIN locations l ON d.location_id = l.location_id 
  WHERE d.department_id IN (
    SELECT department_id 
    FROM employees 
    GROUP BY department_id 
    HAVING COUNT(employee_id) > 10
  );'),

-- 96. Filtro com função de agregação e data
('Liste os nomes dos funcionários que foram contratados no mesmo ano que a média de contratação de todos os funcionários.',
 'SELECT first_name 
  FROM employees 
  WHERE EXTRACT(YEAR FROM hire_date) = (
    SELECT ROUND(AVG(EXTRACT(YEAR FROM hire_date))) 
    FROM employees
  );'),

-- 97. Subconsulta com função de janela
('Exiba os nomes dos funcionários e a diferença entre seus salários e o maior salário do departamento.',
 'SELECT e.first_name, 
         (e.salary - MAX(e.salary) OVER (PARTITION BY e.department_id)) AS diferenca_maior_salario 
  FROM employees e;'),

-- 98. Join múltiplo com COUNT
('Liste os países e a quantidade de departamentos registrados em cada um.',
 'SELECT c.country_name, COUNT(d.department_id) AS total_departamentos 
  FROM countries c 
  JOIN locations l ON c.country_id = l.country_id 
  JOIN departments d ON l.location_id = d.location_id 
  GROUP BY c.country_name;'),

-- 99. Subconsulta correlacionada com EXISTS e funções de data
('Exiba os nomes dos funcionários que começaram a trabalhar após o término do último histórico de trabalho de outros funcionários.',
 'SELECT e.first_name 
  FROM employees e 
  WHERE EXISTS (
    SELECT 1 
    FROM job_history j 
    WHERE j.end_date < e.hire_date
  );'),

-- 100. Join avançado com UNION e agregação
('Liste os nomes das cidades e a soma total de funcionários registrados nelas, incluindo departamentos com ou sem funcionários.',
 'SELECT l.city, COALESCE(SUM(e.employee_id), 0) AS total_funcionarios 
  FROM locations l 
  LEFT JOIN departments d ON l.location_id = d.location_id 
  LEFT JOIN employees e ON d.department_id = e.department_id 
  GROUP BY l.city 
  UNION 
  SELECT ''Outros Locais'', COUNT(*) 
  FROM employees 
  WHERE department_id IS NULL;');
