from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import db


class TaskCreate(BaseModel):
    title: str
    status: bool = False


app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    status: bool


@app.get("/")
def root():
    return {"message": "CLI Task Manager is running"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    rows = db.get_tasks()
    return [Task(id=r[0], title=r[1], status=r[2]) for r in rows]


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    row = db.create_task(task.title, task.status)
    if row is None:
        raise HTTPException(status_code=400, detail="Task could not be created.")
    return Task(id=row[0], title=task.title, status=task.status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    row_count = db.delete_task(task_id)
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Enter a valid row id.")
    return {"message": "task was deleted"}


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task: TaskCreate, task_id: int):
    row = db.update_task(task.title, task.status, task_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return Task(id=row[0], title=task.title, status=task.status)
