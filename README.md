# Python restaurant API Backend

Proyect Python version 3.13.6

## Activate the environment

### Linux/macOS

```sh
source.venv/bin/activate
```

### Windows PowerShell

```ps

.venv\Scripts\Activate.ps1

```

### Windows cmd

```cmd
.venv\Scripts\activate.bat
```

## Ruff formater install

[pypi ruff url](https://pypi.org/project/ruff/)

```sh
 pip install ruff
```

## Alembic SQL migration tool

### Generate migration

Creates a new migration script.

```sh
 alembic revision --autogenerate -m "message"
```

### Apply migration

Updates the DB to latest version.

```sh
 alembic upgrade head
```

### Downgrade

Rolls back changes.

```sh
 alembic downgrade
```

### Check history

Shows migration timeline.

```sh
 alembic history
```
