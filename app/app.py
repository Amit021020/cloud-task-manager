import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, session , Response
from prometheus_client import generate_latest , CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import threading
from dotenv import load_dotenv
app = Flask(__name__)

# Secret key for Flask sessions
app.config["SECRET_KEY"]= os.environ["SECRET_KEY"]

# Prometheus metrics
metrics = PrometheusMetrics(app)

# -------------------------------------------------------------------
# In-memory storage
# -------------------------------------------------------------------

users = {}
tasks = []

next_user_id = 1
next_task_id = 1

data_lock = threading.Lock()


# -------------------------------------------------------------------
# Authentication helper
# -------------------------------------------------------------------

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "username" not in session:
            return redirect(url_for("login_page"))

        return function(*args, **kwargs)

    return decorated_function


# -------------------------------------------------------------------
# Home
# -------------------------------------------------------------------

@app.route("/")
def home():

    if "username" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login_page"))


# -------------------------------------------------------------------
# Login page
# -------------------------------------------------------------------

@app.route("/login", methods=["GET"])
def login_page():

    if "username" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    # Your authentication logic here

    if username == "your_username" and password == "your_password":
        session["username"] = username
        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error="Invalid username or password"
    ), 401

# -------------------------------------------------------------------
# Register page
# -------------------------------------------------------------------

@app.route("/register", methods=["GET"])
def register_page():

    if "username" in session:
        return redirect(url_for("dashboard"))

    return render_template("register.html")


# -------------------------------------------------------------------
# Register API
# -------------------------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register():

    global next_user_id

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username:
        return jsonify({
            "error": "Username is required"
        }), 400

    if len(username) < 3:
        return jsonify({
            "error": "Username must contain at least 3 characters"
        }), 400

    if not password:
        return jsonify({
            "error": "Password is required"
        }), 400

    if len(password) < 6:
        return jsonify({
            "error": "Password must contain at least 6 characters"
        }), 400

    if username in users:
        return jsonify({
            "error": "Username already exists"
        }), 409

    with data_lock:

        users[username] = {
            "id": next_user_id,
            "username": username,
            "password": generate_password_hash(password)
        }

        next_user_id += 1

    return jsonify({
        "message": "Account created successfully"
    }), 201


# -------------------------------------------------------------------
# Login API
# -------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = users.get(username)

    if not user:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    if not check_password_hash(user["password"], password):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    session["username"] = username

    return jsonify({
        "message": "Login successful",
        "username": username
    }), 200


# -------------------------------------------------------------------
# Logout
# -------------------------------------------------------------------

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out successfully"
    }), 200


# -------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# -------------------------------------------------------------------
# Get current user's tasks
# -------------------------------------------------------------------

@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():

    username = session["username"]

    user_tasks = [
        task for task in tasks
        if task["username"] == username
    ]

    return jsonify({
        "tasks": user_tasks
    }), 200


# -------------------------------------------------------------------
# Add task
# -------------------------------------------------------------------

@app.route("/api/tasks", methods=["POST"])
@login_required
def add_task():

    global next_task_id

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    task_name = data.get("task", "").strip()

    if not task_name:
        return jsonify({
            "error": "Task cannot be empty"
        }), 400

    if len(task_name) > 200:
        return jsonify({
            "error": "Task cannot exceed 200 characters"
        }), 400

    username = session["username"]

    with data_lock:

        task = {
            "id": next_task_id,
            "username": username,
            "task": task_name,
            "completed": False
        }

        tasks.append(task)

        next_task_id += 1

    return jsonify({
        "message": "Task added successfully",
        "task": task
    }), 201


# -------------------------------------------------------------------
# Update task
# -------------------------------------------------------------------

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = session["username"]

    for task in tasks:

        if task["id"] == task_id and task["username"] == username:

            if "task" in data:

                task_name = str(data["task"]).strip()

                if not task_name:
                    return jsonify({
                        "error": "Task cannot be empty"
                    }), 400

                task["task"] = task_name

            if "completed" in data:

                if not isinstance(data["completed"], bool):
                    return jsonify({
                        "error": "completed must be true or false"
                    }), 400

                task["completed"] = data["completed"]

            return jsonify({
                "message": "Task updated successfully",
                "task": task
            }), 200

    return jsonify({
        "error": "Task not found"
    }), 404


# -------------------------------------------------------------------
# Delete task
# -------------------------------------------------------------------

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):

    global tasks

    username = session["username"]

    for task in tasks:

        if task["id"] == task_id and task["username"] == username:

            tasks = [
                t for t in tasks
                if not (
                    t["id"] == task_id
                    and t["username"] == username
                )
            ]

            return jsonify({
                "message": "Task deleted successfully"
            }), 200

    return jsonify({
        "error": "Task not found"
    }), 404


# -------------------------------------------------------------------
# Delete all completed tasks
# -------------------------------------------------------------------

@app.route("/api/tasks/completed", methods=["DELETE"])
@login_required
def delete_completed_tasks():

    global tasks

    username = session["username"]

    before = len(tasks)

    tasks = [
        task for task in tasks
        if not (
            task["username"] == username
            and task["completed"]
        )
    ]

    deleted = before - len(tasks)

    return jsonify({
        "message": "Completed tasks deleted",
        "deleted": deleted
    }), 200


# -------------------------------------------------------------------
# Health check
# -------------------------------------------------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    }), 200

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


# -------------------------------------------------------------------
# Run application
# -------------------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )