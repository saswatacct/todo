# SQL tasks

### Given tables:

- tasks (id, name, status, project_id)
- projects (id, name)

### Queries to:

- get all statuses, not repeating, alphabetically ordered

```sql
SELECT DISTINCT
    status
FROM
    tasks
ORDER BY
    status ASC;
```

- get the count of all tasks in each project, order by tasks count descending

```sql
SELECT
    projects.id,
    COUNT(tasks.id) as task_count
FROM
    projects
    INNER JOIN tasks ON projects.id = tasks.project_id
GROUP BY
    projects.id
ORDER BY
    task_count DESC;
```

- get the count of all tasks in each project, order by projects names

```sql
SELECT
    projects.id,
    projects.name,
    COUNT(tasks.id)
FROM
    projects
    INNER JOIN tasks ON projects.id = tasks.project_id
GROUP BY
    projects.id,
    projects.name
ORDER BY
    projects.name;
```

- get the tasks for all projects having the name beginning with "N" letter

```sql
SELECT
    tasks.*
FROM
    tasks
    INNER JOIN projects ON projects.id = tasks.project_id
WHERE
    projects.name LIKE 'N%';
```

- get the list of al projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with project_id= NULL

```sql
SELECT
    projects.*,
    COUNT(tasks.id)
FROM
    projects
    LEFT JOIN tasks ON tasks.project_id = projects.id
WHERE
    projects.name LIKE '%a%'
GROUP BY
    projects.id;
```

- get the list of tasks with duplicate names. Order alphabetically

```sql
SELECT
    tasks.*,
FROM
    tasks
    JOIN (
        SELECT
            name
        FROM
            tasks
        GROUP BY
            name
        HAVING COUNT(*) > 1
    ) AS duplicates ON tasks.name = duplicates.name
ORDER BY
    tasks.name;
```

- get the list of tasks having several exact matches of both name and status, from the project 'Delivery’. Order by matches count

```sql
SELECT
    tasks.name,
    tasks.status,
    COUNT(*) AS match_count
FROM
    tasks
    INNER JOIN projects ON projects.id = tasks.project_id
WHERE
    projects.name = 'Delivery'
GROUP BY
    tasks.name,
    tasks.status
HAVING
    COUNT(*) > 1
ORDER BY
    match_count DESC;
```

- get the list of project names having more than 10 tasks in status 'completed'. Order by project_id

```sql
SELECT
    projects.name
FROM
    projects
    INNER JOIN tasks ON tasks.project_id = projects.id
WHERE
    tasks.status = 'completed'
GROUP BY
    projects.id,
    projects.name
HAVING
    COUNT(tasks.id) > 10
ORDER BY
    projects.id;
```
