apiUrl = "/api/"


document.addEventListener("DOMContentLoaded", () => {
    // Always listening for clicks on the Upload button
    document.querySelector("#uploadBtn").addEventListener("click", () => {
        handle_upload();
    });

    document.getElementById('URLuploadBtn').addEventListener('click', function() {
        const url = document.getElementById('url_article').value;
        fetchAndDisplayURLContent(url);
    });
})


function handle_upload() {
    const summaryPrintSpace = document.getElementById("summaryPrintSpace");
    const fileInput = document.getElementById('file');
    const files = fileInput.files;
    const topicsDropdown = document.getElementById('topics_dd');
    const topicId = topicsDropdown.options[topicsDropdown.selectedIndex].value;

    // Read each first file uploaded in order
    if (files.length > 0) {
        Array.from(files).forEach((file) => {
            console.log("File Name: " + file.name);
            console.log("File Size: " + file.size);
            console.log("File Size: " + (file.size / 1024) + " KB");

            const lastModifiedDate = new Date(file.lastModified);
            console.log("Last Modified: " + lastModifiedDate.toLocaleString());

            // Prepare to read the file contents
            const reader = new FileReader();

            // This function is called when the FileReader has read the file
            reader.onload = function (event) {
                const fileContents = event.target.result;

                // Show a preview of the file uploaded
                document.getElementById("fileContents").innerText = truncateString(fileContents, 400);

                // Show success message 
                $("#fileUploadSuccessMsg").removeClass('d-none')

                // Prepare to call training API
                const data = JSON.stringify({
                    'text': fileContents, 
                    'topic_id': topicId
                });
                const headers = {
                    'Content-Type': 'application/json', 
                    'X-CSRFToken': getCookie('csrftoken'),
                };

                // Call training API
                fetch(apiUrl + 'file_upload_train/', {
                    method: "POST",
                    headers: headers,
                    body: data
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .catch(error => {
                        console.error("Failed to send data to backend:", error);
                    });
                };

            // Read the file as text
            reader.readAsText(file);


        });
    }
}

function fetchAndDisplayURLContent(url) {
    console.log("Within JS function fetchAndDisplayURLContent");
    const topicsDropdown = document.getElementById('topics_dd_url');
    const topicId = topicsDropdown.options[topicsDropdown.selectedIndex].value;

    // Prepare to call training API
    const data = JSON.stringify({
        'url': url,
        'topic_id': topicId
    });
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    };

    // Call training API
    fetch(apiUrl + 'url_fetch_train/', {
        method: "POST",
        headers: headers,
        body: data
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error("Failed to send data to backend:", error);
        });
}
