import psycopg
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_id,
)
import db


class TaskCreate(BaseModel):
    title: str
    status: bool = False


app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    status: bool


class UserCreate(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"message": "CLI Task Manager is running"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(user_id: int = Depends(get_current_user_id)):
    rows = db.get_tasks(user_id)
    return (Task(id=r[0], title=r[1], status=r[2]) for r in rows)


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, user_id: int = Depends(get_current_user_id)):
    row = db.create_task(task.title, task.status, user_id)
    if row is None:
        raise HTTPException(status_code=400, detail="Task could not be created.")
    return Task(id=row[0], title=task.title, status=task.status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id = Depends(get_current_user_id)):
    row_count = db.delete_task(task_id,user_id)
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Enter a valid row id.")
    return {"message": "task was deleted"}


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task: TaskCreate, task_id: int, userid = Depends(get_current_user_id)):
    row = db.update_task(task.title, task.status, task_id, userid)
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return Task(id=row[0], title=task.title, status=task.status)


@app.post("/signup")
def signup(user: UserCreate):
    hashed = hash_password(user.password)
    try:
        db.create_user(user.username, hashed)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User created"}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user(form.username)
    if user is None or not verify_password(form.password, user[2]):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_access_token(user[0])
    return {"access_token": token, "token_type": "bearer"}
