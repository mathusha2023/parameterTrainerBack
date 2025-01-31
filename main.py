from flask import Flask, jsonify, Response, abort
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def make_all_tasks_file():
    tasks = []
    for filename in os.listdir("tasks"):
        if filename.split(".")[0].isdigit():
            with open(f"tasks/{filename}", encoding="UTF-8") as file:
                js = json.load(file)
                tasks.append(js["task"])
    with open("tasks/tasks.json", "w", encoding="UTF-8") as file:
        json.dump(tasks, file, ensure_ascii=False)


@app.route("/")
def index():
    return "OK"


@app.route("/tasks")
def get_tasks():
    response = Response()
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    with open(f"tasks/tasks.json", encoding="UTF-8") as file:
        jsn = file.read()
        response.response = jsn
    return response


@app.route("/tasks/count")
def get_tasks_count():
    count = len(os.listdir("tasks"))
    return jsonify({"count": count})


@app.route("/task/<task_id>")
def get_task_by_id(task_id):
    response = Response()
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    try:
        file = open(f"tasks/{task_id}.json", encoding="UTF-8")
    except FileNotFoundError:
        return abort(404, f"Task with id={task_id} was not found!")
    jsn = file.read()
    response.response = jsn
    file.close()
    return response


if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    make_all_tasks_file()
    app.run(host=host, port=port)
