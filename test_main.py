from fastapi.testclient import TestClient
from main import app
import pytest
import uuid

client = TestClient(app)


def make_user_header():
    """Create a new user everytime and return their auth header"""
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "testpass123"

    client.post("/signup", json={"username": username, "password": password})
    res = client.post("/login", data={"username": username, "password": password})
    assert res.status_code == 200, res.text
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_a():
    return make_user_header()


@pytest.fixture
def user_b():
    return make_user_header()


def test_get_tasks_without_token_returns_401():
    res = client.get("/tasks")
    assert res.status_code == 401


def test_user_cannot_update_another_users_task(user_a, user_b):
    created = client.post("/tasks", json={"title": "A's title"}, headers=user_a)
    print(created.status_code, created.json())
    task_id = created.json()["id"]

    res = client.put(
        f"/tasks/{task_id}", json={"title": "hacked", "status": True}, headers=user_b
    )
    assert res.status_code == 404

    tasks = client.get("/tasks", headers=user_a).json()
    assert tasks[0]["title"] == "A's title"


def test_user_cannot_delete_another_users_task(user_a, user_b):
    created = client.post("/tasks", json={"title": "A's task"}, headers=user_a)
    task_id = created.json()["id"]

    res = client.delete(f"tasks/{task_id}", headers=user_b)
    assert res.status_code == 404

    tasks = client.get("/tasks", headers=user_a).json()
    assert any(t["id"] == task_id for t in tasks)
