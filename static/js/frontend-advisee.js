apiUrl = "/api/"

document.addEventListener("DOMContentLoaded", () => {
    // Select all elements with class research-btn
    const researchBtns = document.querySelectorAll(".research-btn")

    // Loop through each research-btn element and add event listener
    researchBtns.forEach(btn => {
        btn.addEventListener("click", (event) => {
            event.preventDefault()

            let industry = document.getElementById("industry").innerHTML
            let topic = btn.getAttribute("data-topic");
            let researchResultDiv = document.getElementById(topic+'-research-results')

            request_research(industry, topic, researchResultDiv)
        })
    })
})

function request_research(industry, topic, researchResultDiv) {
    const data = JSON.stringify({ 
        'industry': industry,
        'topic': topic,
    });
    const headers = {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken'),};

    fetch(apiUrl + 'research/', {
        method: "POST",
        headers: headers,
        body: data
    })
    .then(response => response.json())
    .then(data => {
        console.log("Research received:", data.message);
        researchResultDiv.innerText = data.message;
    })
    .catch(error => console.error("Failed to fetch data:", error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}