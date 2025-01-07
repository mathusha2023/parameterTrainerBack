from flask import Flask, jsonify, Response, abort
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "OK"


@app.route("/tasks")
def get_tasks():
    response = Response()
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    with open(f"tasks/tasks.json") as file:
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
        file = open(f"tasks/{task_id}.json")
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
    app.run(host=host, port=port)
