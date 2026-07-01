"""Shared pytest fixtures.

Point the app at a throwaway SQLite database *before* importing it, and reset
that database to the seed data before every test so cases stay independent.
"""

import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

# Must be set before `main` is imported (it reads the path at module load).
_TMP_DB = Path(tempfile.mkdtemp()) / "test_recipes.db"
os.environ["RECIPES_DB_PATH"] = str(_TMP_DB)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from seed import init_db, seed_recipes  # noqa: E402


@pytest.fixture(autouse=True)
def reset_db():
    conn = sqlite3.connect(_TMP_DB)
    try:
        init_db(conn)
        seed_recipes(conn)
        conn.commit()
    finally:
        conn.close()
    yield


@pytest.fixture
def client():
    return TestClient(main.app)
