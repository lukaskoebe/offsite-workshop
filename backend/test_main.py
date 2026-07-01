"""API tests for the Recipe Book backend."""

import shutil

from fastapi.testclient import TestClient

import main

SAMPLE = {
    "title": "Test Pancakes",
    "description": "Fluffy test pancakes",
    "image": "",
    "prepTime": 5,
    "cookTime": 15,
    "servings": 4,
    "difficulty": "easy",
    "ingredients": ["flour", "milk", "egg"],
    "instructions": ["mix", "cook"],
}


def test_list_returns_seed(client):
    res = client.get("/api/recipes")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 6
    assert {"id", "title", "prepTime", "cookTime", "difficulty"} <= data[0].keys()
    # list view omits the heavy fields
    assert "ingredients" not in data[0]


def test_get_single(client):
    res = client.get("/api/recipes/1")
    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Spaghetti Carbonara"
    assert isinstance(body["ingredients"], list) and body["ingredients"]


def test_get_missing_returns_404(client):
    assert client.get("/api/recipes/9999").status_code == 404


def test_create_roundtrips(client):
    res = client.post("/api/recipes", json=SAMPLE)
    assert res.status_code == 201
    created = res.json()
    assert created["id"]
    assert created["ingredients"] == ["flour", "milk", "egg"]

    # it now shows up in the list
    listed = client.get("/api/recipes").json()
    assert len(listed) == 7
    assert any(r["title"] == "Test Pancakes" for r in listed)


def test_create_rejects_bad_difficulty(client):
    bad = {**SAMPLE, "difficulty": "spicy"}
    assert client.post("/api/recipes", json=bad).status_code == 422


def test_delete_removes_recipe(client):
    assert client.delete("/api/recipes/1").status_code == 204
    assert client.get("/api/recipes/1").status_code == 404
    assert len(client.get("/api/recipes").json()) == 5


def test_delete_missing_returns_404(client):
    assert client.delete("/api/recipes/9999").status_code == 404


def test_fresh_install_creates_and_seeds_db():
    """A brand-new checkout has no data/ dir; startup must create and seed it."""
    if main.DB_PATH.parent.exists():
        shutil.rmtree(main.DB_PATH.parent)
    assert not main.DB_PATH.exists()

    # Using TestClient as a context manager runs the app's lifespan (ensure_db).
    with TestClient(main.app) as fresh_client:
        res = fresh_client.get("/api/recipes")

    assert res.status_code == 200
    assert len(res.json()) == 6
    assert main.DB_PATH.exists()
