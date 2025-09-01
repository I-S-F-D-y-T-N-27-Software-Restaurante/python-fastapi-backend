# Python restaurant API Backend

Proyect Python version 3.13.6

## Activate the environment

## With MAKE

## Manually

### Linux/macOS

```sh
source.venv/bin/activate
```

### Windows PowerShell

```ps

./venv/Scripts/activate

```

### Windows cmd

```cmd
.venv\Scripts\activate.bat
```

## Install requirements

### Linux/macOS

```sh
pip install -r requirements.txt
```

## Windows

```ps
pip install -r requirements-windows.txt
```

## IMPORTANT: Env setup

User MUST copy .env.example and rename it to .env without deleting original .env.example file. Otherwise proyect wont start.

## Running the proyect

```sh
python ./app/main.py
```

## Optional proyect formater: Ruff formater install

[Link to package at pypi repository.](https://pypi.org/project/ruff/)

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
