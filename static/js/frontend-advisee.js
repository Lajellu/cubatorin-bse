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

    // select all elements with class mark-instruction-as-read
    const markAsReadAnchors = document.querySelectorAll(".mark-instruction-as-read")

    // Loop through each mark-instruction-as-read anchor and add event listener
    markAsReadAnchors.forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault()

            let topicId = link.getAttribute("data-topic-id");

            console.log("marking instructions for topicId " + topicId + " as read")

            markInstructionAsRead(topicId)
        })
    })

})

function markInstructionAsRead(topicId) {
    const data = JSON.stringify({ 
        'topic_id': topicId
    });
    const headers = {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken'),};

    fetch(apiUrl + 'mark_advisee_topic_instruction_read/', {
        method: "POST",
        headers: headers,
        body: data
    })
    .then(response => response.json())
    .then(data => {
        console.log("Mark Instruction As Read response:", data.message);

        // hide the alert div
        $('a.mark-instruction-as-read[data-topic-id="'+topicId+'"]').closest('div')[0].hidden = true
    })
    .catch(error => console.error("Failed to mark instruction as read:", error));
}

function request_research(industry, topic, researchResultDiv) {
    const data = JSON.stringify({ 
        'industry': industry,
        'topic': topic,
    });
    const headers = {
        'Content-Type': 'application/json', 
        'X-CSRFToken': getCookie('csrftoken')
    };

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