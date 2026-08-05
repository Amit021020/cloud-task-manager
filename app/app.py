from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

tasks = []
next_id = 1


@app.route("/")
def home():
    return jsonify({"message": "Cloud Task Manager Running"})


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# Add a task
@app.route("/tasks", methods=["POST"])
def add_task():
    global next_id

    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task field is required"}), 400

    task_name = data["task"].strip()

    if not task_name:
        return jsonify({"error": "Task cannot be empty"}), 400

    task = {
        "id": next_id,
        "task": task_name,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


# Update a task
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()

    for task in tasks:
        if task["id"] == id:

            if "task" in data:
                task["task"] = data["task"].strip()

            if "completed" in data:
                task["completed"] = bool(data["completed"])

            return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404


# Delete a task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tasks

    for task in tasks:
        if task["id"] == id:
            tasks = [t for t in tasks if t["id"] != id]
            return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)