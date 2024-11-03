from flask import Flask, jsonify, Response, abort
import os
from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/")
def index():
    return "OK"


@app.route("/task/<task_id>")
def get_task_by_id(task_id):
    response = Response()
    response.headers["Content-Type"] = "application/json"
    try:
        file = open(f"tasks/{task_id}.json")
    except FileNotFoundError:
        return abort(404, f"Task with id={task_id} was not found!")
    jsn = file.read()
    response.response = jsn
    file.close()
    return response


@app.route("/tasks/count")
def get_tasks_count():
    count = len(os.listdir("tasks"))
    return jsonify({"count": count})


if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    app.run(host=host, port=port)
