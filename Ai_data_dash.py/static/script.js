document.getElementById("uploadBtn").addEventListener("click", function(){

    let fileInput = document.getElementById("fileInput");

    let file = fileInput.files[0];

    let formData = new FormData();

    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        // Update statistics
        document.getElementById("rows").innerText = data.rows;
        document.getElementById("columns").innerText = data.columns;
        document.getElementById("missing").innerText = data.missing;

        createCharts(data);

    });

});



function createCharts(data){

    // Bar Chart
    new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Values",
                data: data.values
            }]
        }
    });


    // Pie Chart
    new Chart(document.getElementById("pieChart"), {
        type: "pie",
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values
            }]
        }
    });


    // Line Chart
    new Chart(document.getElementById("lineChart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Trend",
                data: data.values
            }]
        }
    });

}async function askAI(){

let question = document.getElementById("questionInput").value;

let res = await fetch("/ask_ai",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({question:question})
})

let data = await res.json()

document.getElementById("aiAnswer").innerText = data.answer

}