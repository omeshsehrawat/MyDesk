function addExpenseFunction(e){
    e.preventDefault();
    const expenseItem = document.getElementById("add_item").value.trim();
    const expenseAmount = document.getElementById("add_amount").value;
    const expenseDate = document.getElementById("expense_date").value;
    if (expenseItem === "" || expenseAmount === "" || expenseDate === "") return closeExpenseForm();

    fetch('/add_expense', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item: expenseItem, amount: expenseAmount, date: expenseDate})
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
        alert("Expense added successfully!");
        loadExpense();
    })
    .catch(err => console.error("Error adding expense:", err));
    
    document.getElementById("add_item").value = "";
    document.getElementById("add_amount").value = "";
    document.getElementById("expense_date").value = "";
    closeExpenseForm();
}

function loadExpense(){
    fetch("/expenditure")
    .then(res => res.json())
    .then(expenses => {
        const tbody = document.getElementById("expenseTableBody");
        tbody.innerHTML ="";
        expenses.forEach((row, index) => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${row[1]}</td>
                <td>${row[2]}</td>
                <td>${row[3]}</td>
                <td>${row[4]}</td>
                <td>
                    <button onclick="deleteExpense(${row[0]})">✖</button>
                </td>
            `;
            // Apply alternate background color
            if (index % 2 === 0) {
                tr.style.backgroundColor = "#ffffffff"; // white
            } else {
                tr.style.backgroundColor = "#dadbd9ff"; // light gray
            }
            tbody.appendChild(tr);
        });
    })
    .catch(err => console.error("Error loading expenses:", err));
}

function deleteExpense(sr_no){
    fetch(`/delete_expense/${sr_no}`, {method: "DELETE"})
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
        alert("Expense deleted successfully!");
        loadExpense();
    })
    .catch(err => console.error("Error deleting expense:", err));
}

function expenseFormPopup(){
    document.getElementById("expenseForm").style.display = "block";
}

function closeExpenseForm(){
    document.getElementById("expenseForm").style.display = "none";
}

window.onload = loadExpense;