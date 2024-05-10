document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#uploadBtn").addEventListener("click", () => {
        handle_upload();
    });

     document.querySelector("#testMe").addEventListener("click", () => {
         fetch('http://127.0.0.1:5000/get_message')
            .then(response => response.json())
            .then(data => {
                // Add newlines to the OpenAI API response
                let formattedMessage = data.message.replace(/\.(\s+)/g, '.$1<br>');
                formattedMessage = formattedMessage.replace(/([a-z]\))(\s+)/g, '<br>$1$2');
                document.getElementById('apiMessageSpace').innerHTML = formattedMessage;
            })
            .catch(error => console.error('Error fetching data:', error));
    });

})

function handle_upload() {
    const summaryPrintSpace = document.getElementById("summaryPrintSpace");
    const fileInput = document.getElementById('file');
    const files = fileInput.files;

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

            reader.onload = function (event) {
                // This function is called when the FileReader has read the file
                const fileContents = event.target.result;
                document.getElementById("fileContents").innerText = truncateString(fileContents, 400);
                const data = JSON.stringify({'text': fileContents});
                const headers = {'Content-Type': 'application/json'};

                // Using fetch API to send the file content to the backend
                fetch('http://127.0.0.1:5000/api/upload_summarize_train', {
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
                    .then(data => {
                        const targetDiv = document.getElementById("summaryPrintSpace");
                        console.log("Test");
                        console.log("TODO Summary received: ", data.completion);
                        targetDiv.innerText = data.completion;
                        // Reset file input after the last file is processed
                        if (index === files.length - 1) {
                            fileInput.value = ''; // Reset the file input here
                        }
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

// truncateString: written byFreeCodeCamp
function truncateString(str, num) {
  if (str.length > num) {
    return str.slice(0, num) + "...";
  } else {
    return str;
  }
}