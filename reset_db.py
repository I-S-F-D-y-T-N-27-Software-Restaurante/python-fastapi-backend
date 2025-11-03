import subprocess
from pathlib import Path

# Project root (adjust if your script is in a subfolder)
project_root = Path(__file__).parent.resolve()
db_file = project_root / "app/data/database.sqlite"

# Step 1: Delete the old database if it exists
if db_file.exists():
    db_file.unlink()
    print("Deleted existing database.sqlite")

# Step 2: Do NOT create the file manually; Alembic/SQLAlchemy will handle it

# Step 3: Upgrade the database to the latest revision
# This will create a fresh DB with all tables and apply migrations
subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=project_root)
print("Database recreated and all migrations applied")
