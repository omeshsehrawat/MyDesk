function addTaskFunction(e) {
    e.preventDefault();
    const taskText = document.getElementById("add_task").value.trim();
    const deadline = document.getElementById("myDate").value;
    if (taskText === "") return closeForm();

    fetch('/add_task', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: taskText, myDate: deadline })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
        alert("Task added successfully!");
        loadTasks();
    })
    .catch(err => console.error("Error adding task:", err));

    document.getElementById("add_task").value = "";
    document.getElementById("myDate").value = "";
    closeForm();
}

function loadTasks() {
    fetch("/tasks")
    .then(res => res.json())
    .then(tasks => {
        const tbody = document.getElementById("taskTableBody");
        tbody.innerHTML = "";
        tasks.forEach((row, index) => {
            const tr = document.createElement("tr");

            if (row[4] === "pending") {
                tr.style.backgroundColor = "#fecaca";   // light red
            } else if (row[4] === "done") {
                tr.style.backgroundColor = "#bbf7d0";   // light green
            }

            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${row[1]}</td>
                <td>${row[2]}</td>
                <td>${row[3]}</td>
                <td>
                    <select onchange="updateStatus(${row[0]}, this.value)">
                        <option value="pending" ${row[4] === "pending" ? "selected" : ""}>Pending</option>
                        <option value="done" ${row[4] === "done" ? "selected" : ""}>Done</option>
                    </select>
                </td>
                <td>
                    <button onclick="deleteTask(${row[0]})">✖</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    })
    .catch(err => console.error("Error loading tasks:", err));
}

function deleteTask(sr_no) {
    fetch(`/delete/${sr_no}`, { method: "DELETE" })
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
        alert("Task deleted successfully!");
        loadTasks();
    })
    .catch(err => console.error("Error deleting task:", err));
}

function updateStatus(sr_no, status) {
    const select = document.querySelector(`#taskTableBody select[onchange*="${sr_no}"]`);
    if (select) {
        const tr = select.closest("tr");
        if (status === "pending") {
            tr.style.backgroundColor = "#fecaca"; // red
        } else if (status === "done") {
            tr.style.backgroundColor = "#bbf7d0"; // green
        }
    }
    fetch(`/update/${sr_no}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: status })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(err => console.error("Error updating task:", err));
}

function taskFormPopup() {
    document.getElementById("taskForm").style.display = "block";
}

function closeForm() {
    document.getElementById("taskForm").style.display = "none";
}

window.onload = loadTasks;
