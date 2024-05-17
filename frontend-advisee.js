document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#cubatorin-research-btn").addEventListener("click", () => {
        let industry = "parking" // TODO: Get from form
        let topic = "market sizing" // TODO: Get from form
        request_research(industry, topic);
    });

})

function request_research(industry, topic) {
    const data = JSON.stringify({ text: "Please find the market demographic usually used in the " + industry + " industry" });
    const headers = {'Content-Type': 'application/json'};

    fetch('http://159.65.182.82:5000/api/research', {
        method: "POST",
        headers: headers,
        body: data
    })
    .then(response => response.json())
    .then(data => {
        console.log("Research received:", data.message);
        const targetDiv = document.getElementById("research-results-space");
        targetDiv.innerText = data.message;
    })
    .catch(error => console.error("Failed to fetch data:", error));
}

