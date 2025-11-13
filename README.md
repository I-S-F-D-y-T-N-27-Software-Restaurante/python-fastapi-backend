# Python restaurant API Backend

Proyect Python version 3.13.6

## Activate the environment

## With MAKE

First execute to list available commands:

```sh
make help
```

After python vevn link and .env file setup:

```sh
make run
```

## Manually

### Crear venv

```cmd

python -m venv venv

```

## Activación

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
python -m app.main
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

## Test Requests with REST Client extension

On dev/request/main.http you will find a file with request that can be tested and previewed live with one click using the REST VSCode extension recommended in .vscode workspace recomendations: humao.rest-client
