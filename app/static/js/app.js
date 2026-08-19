document.addEventListener("DOMContentLoaded", () => {

    // =========================================================
    // LOGIN
    // =========================================================

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {

        loginForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const username =
                document.getElementById("username").value.trim();

            const password =
                document.getElementById("password").value;

            const message =
                document.getElementById("loginMessage");

            try {

                const response = await fetch("/api/login", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        password
                    })

                });

                const data = await response.json();

                if (!response.ok) {

                    message.textContent =
                        data.error || "Login failed";

                    message.style.color = "#dc2626";

                    return;
                }

                message.textContent =
                    "Login successful. Redirecting...";

                message.style.color = "#16a34a";

                setTimeout(() => {

                    window.location.href = "/dashboard";

                }, 500);

            } catch (error) {

                message.textContent =
                    "Unable to connect to server";

                message.style.color = "#dc2626";
            }

        });
    }


    // =========================================================
    // REGISTER
    // =========================================================

    const registerForm =
        document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const username =
                    document
                        .getElementById("registerUsername")
                        .value
                        .trim();

                const password =
                    document
                        .getElementById("registerPassword")
                        .value;

                const confirmPassword =
                    document
                        .getElementById("confirmPassword")
                        .value;

                const message =
                    document.getElementById(
                        "registerMessage"
                    );


                if (password !== confirmPassword) {

                    message.textContent =
                        "Passwords do not match";

                    message.style.color = "#dc2626";

                    return;
                }


                try {

                    const response = await fetch(
                        "/api/register",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                username,
                                password
                            })

                        }
                    );


                    const data =
                        await response.json();


                    if (!response.ok) {

                        message.textContent =
                            data.error ||
                            "Registration failed";

                        message.style.color =
                            "#dc2626";

                        return;
                    }


                    message.textContent =
                        "Account created! Redirecting to login...";

                    message.style.color =
                        "#16a34a";


                    setTimeout(() => {

                        window.location.href =
                            "/login";

                    }, 800);


                } catch (error) {

                    message.textContent =
                        "Unable to connect to server";

                    message.style.color =
                        "#dc2626";
                }

            }
        );
    }


    // =========================================================
    // DASHBOARD
    // =========================================================

    const taskList =
        document.getElementById("taskList");

    if (taskList) {

        loadTasks();

    }


    // =========================================================
    // ADD TASK
    // =========================================================

    const taskForm =
        document.getElementById("taskForm");

    if (taskForm) {

        taskForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const input =
                    document.getElementById("taskInput");

                const task =
                    input.value.trim();


                if (!task) {
                    return;
                }


                try {

                    const response =
                        await fetch("/api/tasks", {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                task
                            })

                        });


                    const data =
                        await response.json();


                    if (!response.ok) {

                        showToast(
                            data.error ||
                            "Unable to add task"
                        );

                        return;
                    }


                    input.value = "";

                    showToast(
                        "Task added successfully"
                    );

                    loadTasks();


                } catch (error) {

                    showToast(
                        "Unable to connect to server"
                    );
                }

            }
        );
    }


    // =========================================================
    // CLEAR COMPLETED
    // =========================================================

    const clearButton =
        document.getElementById(
            "clearCompletedBtn"
        );


    if (clearButton) {

        clearButton.addEventListener(
            "click",
            async () => {

                try {

                    const response =
                        await fetch(
                            "/api/tasks/completed",
                            {
                                method: "DELETE"
                            }
                        );


                    const data =
                        await response.json();


                    if (!response.ok) {

                        showToast(
                            data.error ||
                            "Unable to delete tasks"
                        );

                        return;
                    }


                    showToast(
                        `${data.deleted} completed task(s) deleted`
                    );


                    loadTasks();


                } catch (error) {

                    showToast(
                        "Unable to connect to server"
                    );
                }

            }
        );
    }


    // =========================================================
    // LOGOUT
    // =========================================================

    const logoutButton =
        document.getElementById("logoutBtn");


    if (logoutButton) {

        logoutButton.addEventListener(
            "click",
            async () => {

                try {

                    await fetch(
                        "/logout",
                        {
                            method: "POST"
                        }
                    );

                    window.location.href =
                        "/login";

                } catch (error) {

                    window.location.href =
                        "/login";
                }

            }
        );
    }

});


// =============================================================
// LOAD TASKS
// =============================================================

async function loadTasks() {

    const taskList =
        document.getElementById("taskList");

    if (!taskList) {
        return;
    }


    taskList.innerHTML =
        '<div class="loading">Loading tasks...</div>';


    try {

        const response =
            await fetch("/api/tasks");


        if (response.status === 401) {

            window.location.href =
                "/login";

            return;
        }


        const data =
            await response.json();


        renderTasks(data.tasks);


    } catch (error) {

        taskList.innerHTML = `
            <div class="empty-state">
                Unable to load tasks.
            </div>
        `;

    }

}


// =============================================================
// RENDER TASKS
// =============================================================

function renderTasks(tasks) {

    const taskList =
        document.getElementById("taskList");


    if (!tasks || tasks.length === 0) {

        taskList.innerHTML = `
            <div class="empty-state">

                <div class="empty-state-icon">
                    📝
                </div>

                <h3>
                    No tasks yet
                </h3>

                <p>
                    Add your first task above.
                </p>

            </div>
        `;

        updateStats([]);

        return;
    }


    taskList.innerHTML = "";


    tasks.forEach(task => {

        const item =
            document.createElement("div");


        item.className =
            "task-item" +
            (task.completed
                ? " completed"
                : "");


        item.innerHTML = `

            <input
                type="checkbox"
                class="task-checkbox"
                ${task.completed ? "checked" : ""}
                onchange="toggleTask(
                    ${task.id},
                    this.checked
                )"
            >

            <div class="task-content">

                <div class="task-name">
                    ${escapeHtml(task.task)}
                </div>

            </div>

            <div class="task-actions">

                <button
                    class="delete-btn"
                    onclick="deleteTask(${task.id})"
                >
                    Delete
                </button>

            </div>

        `;


        taskList.appendChild(item);

    });


    updateStats(tasks);
}


// =============================================================
// TOGGLE TASK
// =============================================================

async function toggleTask(taskId, completed) {

    try {

        const response =
            await fetch(
                `/api/tasks/${taskId}`,
                {

                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        completed
                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showToast(
                data.error ||
                "Unable to update task"
            );

            return;
        }


        showToast(
            completed
                ? "Task completed ✓"
                : "Task marked as pending"
        );


        loadTasks();


    } catch (error) {

        showToast(
            "Unable to connect to server"
        );

    }

}


// =============================================================
// DELETE TASK
// =============================================================

async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `/api/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showToast(
                data.error ||
                "Unable to delete task"
            );

            return;
        }


        showToast(
            "Task deleted successfully"
        );


        loadTasks();


    } catch (error) {

        showToast(
            "Unable to connect to server"
        );

    }

}


// =============================================================
// UPDATE STATISTICS
// =============================================================

function updateStats(tasks) {

    const total =
        tasks.length;


    const completed =
        tasks.filter(
            task => task.completed
        ).length;


    const pending =
        total - completed;


    const totalElement =
        document.getElementById(
            "totalTasks"
        );


    const pendingElement =
        document.getElementById(
            "pendingTasks"
        );


    const completedElement =
        document.getElementById(
            "completedTasks"
        );


    if (totalElement) {

        totalElement.textContent =
            total;
    }


    if (pendingElement) {

        pendingElement.textContent =
            pending;
    }


    if (completedElement) {

        completedElement.textContent =
            completed;
    }

}


// =============================================================
// TOAST
// =============================================================

function showToast(message) {

    const toast =
        document.getElementById("toast");


    if (!toast) {
        return;
    }


    toast.textContent =
        message;


    toast.classList.add("show");


    setTimeout(() => {

        toast.classList.remove("show");

    }, 2500);

}


// =============================================================
// HTML ESCAPE
// =============================================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}