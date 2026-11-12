import psycopg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:3001@localhost:5432/tasksdb",
)


def get_connection():
    return psycopg.connect(DATABASE_URL)


def get_tasks(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select id,title,status from tasks where user_id = %s;", (user_id,)
            )
            return cur.fetchall()


def create_task(title: str, status: bool, id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "insert into tasks(title,status,user_id) values (%s,%s,%s) returning id",
                (title, status, id),
            )
            row = cur.fetchone()
    return row


def update_task(title, status, task_id, userid):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "update tasks set title = %s,status = %s where id = %s and user_id = %s returning id;",
                (title, status, task_id, userid),
            )
            row = cur.fetchone()
    return row


def delete_task(task_id, userid):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "delete from tasks where id = %s AND user_id = %s returning id",
                (task_id, userid),
            )
            return cur.rowcount


def create_user(username: str, hashed_password: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "insert into users(username,hashed_password) values(%s,%s)",
                (username, hashed_password),
            )


def get_user(username: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "Select id,username,hashed_password from users where username =%s ",
                (username,),
            )
            return cur.fetchone()
