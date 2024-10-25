apiUrl = "/api/"


document.addEventListener("DOMContentLoaded", () => {
    // // Always listening for clicks on the Upload button
    // document.querySelector("#uploadBtn").addEventListener("click", () => {
    //     handle_upload();
    // });

    // document.getElementById('URLuploadBtn').addEventListener('click', function() {
    //     const url = document.getElementById('url_article').value;
    //     fetchAndDisplayURLContent(url);
    // });

    // Always listening for clicks on the File Upload button
    $("#uploadBtn").click(() => {
        handle_upload();
    });

    // Always listening for clicks on the URL Upload button
    $('#URLuploadBtn').click(() => {
        const url = $('#url_article').val();
        fetchAndDisplayURLContent(url);
    });

    // Always listening for clicks on the Raw Text Upload button
    $('#rawTextUploadBtn').click(() => {
        console.log("rawTextUploadBtn: Clicked");
        const raw_text = $('#rawText').val();
        handle_raw_text_upload(raw_text);
    });
})

function handle_raw_text_upload() {
    console.log("handle_raw_text_upload")
    const rawText = $('#rawText').val().trim();
    if(rawText === ""){
        console.error("Cannot leave raw text box blank");
        $("#rawTextUploadErrorMsg").removeClass('d-none');
        $("#rawTextUploadSuccessMsg").addClass('d-none');
        return
    }

    console.log(rawText)
    const topicsDropdown = document.getElementById('topics_dd_raw');
    const topicId = topicsDropdown.options[topicsDropdown.selectedIndex].value;
    console.log(topicId)

    // Prepare to call training API
    const data = JSON.stringify({
        'text': rawText, 
        'topic_id': topicId
    });
    const headers = {
        'Content-Type': 'application/json', 
        'X-CSRFToken': getCookie('csrftoken'),
    };

    console.log("About to fetch API: raw_text_upload_train")
    // Call training API
    fetch(apiUrl + 'raw_text_upload_train/', {
        method: "POST",
        headers: headers,
        body: data
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('The text box cannot be left empty.');
            } else {
                // If the response scraping the webpage succeeded
                console.log(response)
                $("#rawTextUploadErrorMsg").addClass('d-none')
                $("#rawTextUploadSuccessMsg").removeClass('d-none')
            }
            return response.json();
        })
        .catch(error => {
            console.error("Will not be able to train on the data in the URL provided. Error: ", error);
            $("#rawTextUploadErrorMsg").removeClass('d-none')
            $("#rawTextUploadSuccessMsg").addClass('d-none')
        });

        // .then(response => {
        //     if (!response.ok) {
        //         throw new Error('Network response was not ok');
        //     } else {
        //         console.log("Network response was ok")
        //         return response.json();
        //     }
            
        // })
        // .catch(error => {
        //     console.error("Failed to send data to backend:", error);
        // });
}

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
    console.log("Within JS function fetchAndDisplayURLContent " + url);
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
                throw new Error('The URL was not correctly written, or the URL does not contain data. Please correct the URL or try another URL.');
            } else {
                // If the response scraping the webpage succeeded
                console.log(response)
                $("#urlUploadErrorMsg").addClass('d-none')
                $("#urlUploadSuccessMsg").removeClass('d-none')
            }
            return response.json();
        })
        .catch(error => {
            console.error("Will not be able to train on the data in the URL provided. Error: ", error);
            $("#urlUploadErrorMsg").removeClass('d-none')
            $("#urlUploadSuccessMsg").addClass('d-none')
        });
}
