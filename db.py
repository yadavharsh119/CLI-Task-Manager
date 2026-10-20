import psycopg


def get_connection():
    return psycopg.connect("host=localhost user=postgres password=3001 dbname=tasksdb")


def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select id,title,status from tasks;")
            return cur.fetchall()


def create_task(title, status):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "insert into tasks(title,status) values (%s,%s) returning id",
                (title, status),
            )
            row = cur.fetchone()
    return row


def update_task(title, status, task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "update tasks set title = %s,status = %s where id = %s returning id",
                (title, status, task_id),
            )
            row = cur.fetchone()
    return row


def delete_task(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("delete from tasks where id = %s", (task_id,))
            return cur.rowcount
