from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []


@app.route("/")
def home():
    return "Cloud Task Manager Running"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.json

    task = {
        "id": len(tasks)+1,
        "task": data["task"]
    }

    tasks.append(task)

    return jsonify(task)


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    global tasks

    tasks = [
        task for task in tasks
        if task["id"] != id
    ]

    return jsonify({
        "message":"Task deleted"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)