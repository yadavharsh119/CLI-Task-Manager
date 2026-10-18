from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import psycopg


class TaskCreate(BaseModel):
    title: str
    status: bool = False


app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    status: bool


def get_connection():
    return psycopg.connect(
        host="localhost", dbname="tasksdb", user="postgres", password="3001"
    )


def load_tasks():
    with open("tasks.json", "r") as file:
        return json.load(file)


@app.get("/")
def root():
    return {"CLI Task Manager is running"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select id,title,status from tasks;")
            rows = cur.fetchall()
    return [Task(id=r[0], title=r[1], status=r[2]) for r in rows]


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "insert into tasks (title,status) values (%s,%s) returning id; ",
        (task.title, task.status),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Row could not be created")
    new_id = row[0]
    conn.commit()
    cur.close()
    conn.close()
    return Task(id=new_id, title=task.title, status=task.status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("delete from tasks where id = %s;", (task_id,))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Enter a valid row id.")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "task was deleted"}


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task: TaskCreate, task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "update tasks set title = %s, status = %s where id = %s returning id;",
        (task.title, task.status, task_id),
    )
    updated_row = cur.fetchone()
    if updated_row is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found.")
    updated_id = updated_row[0]
    conn.commit()
    cur.close()
    conn.close()
    return Task(id=updated_id, title=task.title, status=task.stgatus)