import json

task_list = []


def add_task():
    id = int(input("Enter your id:"))
    title = input("Enter your title:")
    status_input = input("Enter your status(true,false): ").strip().lower()
    status = status_input == "true"
    task = {"id": id, "title": title, "status": status}
    task_list.append(task)


def lists_tasks():
    for task in task_list:
        print(task)


def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(task_list, file)
    file.close()


def load_tasks():
    with open("tasks.json", "r") as file:
        task_list.extend(json.load(file))


def delete_tasks():
    delete_task = int(input("Enter task id:"))
    found = False
    for task in task_list:
        if task["id"] == delete_task:
            task_list.remove(task)
            found = True
            break
    if found:
        print("ID has been deleted")
    else:
        print("ID was not found")
    save_tasks()


def update_tasks():
    update_task = int(input("Enter task id: "))
    found = False
    for task in task_list:
        if task["id"] == update_task:
            found = True
            task_attribute = input("enter the attribute to update: ")
            if task_attribute == "id":
                task["id"] = int(input("Enter new id: "))
            elif task_attribute == "title":
                task["title"] = input("Enter new title: ")
            elif task_attribute == "status":
                status_input = input("Enter new status: ").strip().lower()
                task["status"] = status_input == "true"
            else:
                print("Enter a valid attribute")
                found = False
                break
    if found:
        print("Update was successful")
        save_tasks()
    else:
        print("Enter a valid id")


load_tasks()
while True:
    user = input("Action(add,print,update,delete,exit) : ")
    if user == "add":
        add_task()
        save_tasks()
    elif user == "print":
        lists_tasks()
    elif user == "delete":
        delete_tasks()
    elif user == "update":
        update_tasks()
    elif user == "exit":
        save_tasks()
        break
    else:
        print("Enter a valid action")
lists_tasks()