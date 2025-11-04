function generateReportFunction() {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const option = document.querySelector("input[name='option']:checked")?.value;

    if(!startDate || !endDate || !option) {
        alert("Please fill all fields");
        return;
    }

    fetch('/get_report',{
        method: "POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({startDate, endDate, option})
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById("tableWrapper");
        const oldTable = document.getElementById("reportTable");

        if(oldTable) 
            oldTable.remove();

        const table = document.createElement("table");
        table.id="reportTable";
        
        let headers = [];
        if(option === "todo"){
            headers = ["ID", "Task", "Date", "Deadline", "Status"];
        }
        else if(option === "expense"){
            headers = ["ID", "Item", "Amount", "Date", "Entry Date"];
        }

        const thead = table.createTHead();
        const headerRow = thead.insertRow();
        headers.forEach(h =>{
            const th = document.createElement("th");
            th.innerText = h;
            headerRow.appendChild(th);
        });

        const tbody = table.createTBody();
        data.forEach(row => {
            const tr = tbody.insertRow();
            row.forEach(cell => {
                const td = tr.insertCell();
                td.innerText = cell;
                tr.appendChild(td);
            });
        });
        container.appendChild(table);
        createChart(data, option);
        document.getElementById("downloadBtn").style.display = "block";
        document.getElementById("chartWrapper").style.display = "flex";
        document.getElementById("reportChart").style.display = "block";

    })
    .catch(error => {
        console.error("Error generating report:", error);
        alert("Failed to generate report. Please try again.");
    });
    
}

function showDownloadOptions() {
    const optionsDiv = document.getElementById("downloadOptions")
    optionsDiv.style.display = optionsDiv.style.display === "none" ? "block" : "none";
}

function downloadCSV() {
    let table = document.getElementById("reportTable");
    let rows = table.querySelectorAll("tr");
    let csv = [];

    rows.forEach(row => {
        let cols = row.querySelectorAll("td, th");
        let rowData = [];
        cols.forEach(col => rowData.push(col.innerText));
        csv.push(rowData.join(","));
    });

    let csvFile = new Blob([csv.join("\n")], {type: "text/csv"});
    let downloadLink = document.createElement("a");
    downloadLink.download = "report.csv";
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.click();

    document.getElementById("downloadOptions").style.display = "none";
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text("Report", 14, 16);
    doc.autoTable({
        html: "#reportTable",
        startY: 20,
        theme: "grid",
        styles: { fontSize: 10 }
    });

    if(reportChart){
        const chartImage = reportChart.toBase64Image();
        const finalY = doc.lastAutoTable.finalY + 10; //space after table
        doc.addImage(chartImage, 'PNG', 14, finalY, 100, 100);
    }

    doc.save("report.pdf");

    document.getElementById("downloadOptions").style.display = "none";
}

// Chart part
// Register plugin globally once
Chart.register(ChartDataLabels);

let reportChart = null;
function createChart(data, option){
    const ctx = document.getElementById("reportChart").getContext("2d");

    if(reportChart){
        reportChart.destroy();
    }

    let labels = [];
    let values = [];

    if(option === "todo"){
        const statusCount = {};
        data.forEach(row => {
            const status = row[4];
            statusCount[status] = (statusCount[status] || 0) + 1;
        });
        labels = Object.keys(statusCount);
        values = Object.values(statusCount);
    }
    else if(option === "expense"){
        const categorySum = {};
        data.forEach(row => {
            const category = row[1];   // Item name
            const amount = parseFloat(row[2]);
            categorySum[category] = (categorySum[category] || 0) + amount;
        });
        labels = Object.keys(categorySum);
        values = Object.values(categorySum);
    }

    reportChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: option === "todo" ? "Tasks Count" : "Expense Amount",
                data: values,
                backgroundColor: [
                    'rgba(79, 70, 229, 0.6)',
                    'rgba(239, 68, 68, 0.6)',
                    'rgba(16, 185, 129, 0.6)',
                    'rgba(250, 204, 21, 0.6)',
                    'rgba(14, 165, 233, 0.6)',
                    'rgba(168, 85, 247, 0.6)'
                ],
                borderColor: [
                    'rgba(79, 70, 229, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(250, 204, 21, 1)',
                    'rgba(14, 165, 233, 1)',
                    'rgba(168, 85, 247, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                },
                tooltip: {
                    callbacks:{
                        label: function(context){
                            let label = context.label || '';
                            let value = context.raw || 0;
                            let total = context.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                },
                datalabels: {
                    color: '#000',
                    font: { weight: 'bold', size: 12 },
                    formatter: (value, ctx) => {
                        let total = ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                        let percentage = ((value / total) * 100).toFixed(1);
                        return `${value} (${percentage}%)`;
                    }
                }
            }
        }
    });
}
