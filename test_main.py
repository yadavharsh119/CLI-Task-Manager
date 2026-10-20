from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_code():
    response = client.get("/")
    assert response.status_code == 200


def test_create_and_delete_task():
    create = client.post("/tasks", json={"title": "test", "status": False})
    assert create.status_code == 200
    task_id = create.json()["id"]

    delete = client.delete(f"/tasks/{task_id}")
    assert delete.status_code == 200

    delete_again = client.delete(f"/tasks/{task_id}")
    assert delete_again.status_code == 404
