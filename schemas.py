from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    status: bool = False


class Task(BaseModel):
    id: int
    title: str
    status: bool


class UserCreate(BaseModel):
    username: str
    password: str
