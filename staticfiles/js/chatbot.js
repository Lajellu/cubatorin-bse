apiUrl = "/api/"

$(document).ready(() => {
    $("#promptButton").click(() => {   
        promptChatbot();
    });
});

function promptChatbot() {
    console.log("Inside promptChatbot function")
    const promptText = $("#promptText").val()
    console.log(promptText)

    // Create a new element for the prompt just sent
    let chatHistoryPrompt = $(`
        <div class="container mt-4">
            <div class="row justify-content-end">
                <div class="card col-8" style="width: 18rem; background-color:#E7F3F9">
                    <div class="card-body">
                        <p class="card-text">
                            <pre style='white-space: pre-wrap'> ${promptText} </pre> 
                        </p>
                    </div>
                </div>
            </div>
        </div>    
        `);
        

    $("#chatHistory").prepend(chatHistoryPrompt);

    // Prepare to call prompting API
    const data = JSON.stringify({
        'text': promptText
    });
    const headers = {
        'Content-Type': 'application/json', 
        'X-CSRFToken': getCookie('csrftoken'),
    };

    // Call prompting API
    fetch(apiUrl + 'promptChatbot/', {
        method: "POST",
        headers: headers,
        body: data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json()

    })
    .then(data => {
        console.log("Chatbot response", data.message);
        //document.getElementById("chatbotResponse").innerText = data.message;
        // $("#chatbotResponse").text(data.message)

        // Create a new element for the chatbot response
        let chatHistoryPrompt = $(`
            <div class="container mt-4">
                <div class="row justify-content-start">
                    <div class="card col-8" style="width: 18rem;">
                        <div class="card-body">
                            <p class="card-text">
                                <pre style='white-space: pre-wrap'> ${data.message} </pre> 
                            </p>
                        </div>
                    </div>
                </div>
            </div>    
            `);

        $("#chatHistory").prepend(chatHistoryPrompt);
    })
    .catch(error => {
        console.error("Failed to send data to backend:", error);
    });

};
