document.addEventListener("DOMContentLoaded", () => {
    // Always listening for clicks on the Upload button
    document.querySelector("#uploadBtn").addEventListener("click", () => {
        handle_upload();
    });

    // Always listening for clicks on the Test Me button
     document.querySelector("#testMe").addEventListener("click", () => {
         console.log("Test Me button clicked");

         fetch('http://cubatorin.com:5000/test_me')
            .then(response => {
                console.log("Received response from server");  // Add this line
                return response.json();
            })
            .then(data => {
                console.log("Sending request to the summarizer");
                console.log(data);  // Add this line to see the received data
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
                fetch('http://cubatorin.com:5000/api/upload_summarize_train', {
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

function fetchAndDisplayURLContent(url) {
    const proxyUrl = 'http://cubatorin.com:5000/fetch_url_data?url=' + encodeURIComponent(url);

    fetch(proxyUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            } else {
                console.log("The response was OK");
                return response.text();
            }
        })
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');
            const textContent = doc.body.innerText;
            document.getElementById('fileContents').innerText = textContent;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            document.getElementById('fileContents').innerText = 'Failed to fetch content from the URL.';
        });
}


// Function for filling in the bar graph for the number of articles uploaded for each topic
function fillBarGraphs(){
    // JS for filling in the bar graph for the number of articles uploaded for each topic
    let numMarketSizing = 30;
    let numProductMarketFit = 0;
    let numValuation = 0;
    let numCapitalization = 0;
    let numCompetitiveAnalysis = 0;
    let numContentMarketing = 0;
    let numNetworking = 0;
    let numCustomerJourney = 0;
    let numPrivacyandDataCompliance = 0;
    let numCustomerLifetimeValue = 0;
    let numSaaSMetrics = 0;

    document.getElementById("barMarketSizing").innerHTML = numMarketSizing + "%";
    document.getElementById("progressMarketSizing").style.width = numMarketSizing + "%";
    document.getElementById("progressMarketSizing").ariaValueNow = numMarketSizing.toString();

    document.getElementById("barProductMarketFit").innerHTML = numProductMarketFit + "%";
    document.getElementById("progressProductMarketFit").style.width = numProductMarketFit + "%";
    document.getElementById("progressProductMarketFit").ariaValueNow = numProductMarketFit.toString();

    document.getElementById("barValuation").innerHTML = numValuation + "%";
    document.getElementById("progressValuation").style.width = numValuation + "%";
    document.getElementById("progressValuation").ariaValueNow = numValuation.toString();

    document.getElementById("barCapitalization").innerHTML = numCapitalization + "%";
    document.getElementById("progressCapitalization").style.width = numCapitalization + "%";
    document.getElementById("progressCapitalization").ariaValueNow = numCapitalization.toString();

    document.getElementById("barCompetitiveAnalysis").innerHTML = numCompetitiveAnalysis + "%";
    document.getElementById("progressCompetitiveAnalysis").style.width = numCompetitiveAnalysis + "%";
    document.getElementById("progressCompetitiveAnalysis").ariaValueNow = numCompetitiveAnalysis.toString();

    document.getElementById("barContentMarketing").innerHTML = numContentMarketing + "%";
    document.getElementById("progressContentMarketing").style.width = numContentMarketing + "%";
    document.getElementById("progressContentMarketing").ariaValueNow = numContentMarketing.toString();

    document.getElementById("barNetworking").innerHTML = numNetworking + "%";
    document.getElementById("progressNetworking").style.width = numNetworking + "%";
    document.getElementById("progressNetworking").ariaValueNow = numNetworking.toString();

    document.getElementById("barCustomerJourney").innerHTML = numCustomerJourney + "%";
    document.getElementById("progressCustomerJourney").style.width = numCustomerJourney + "%";
    document.getElementById("progressCustomerJourney").ariaValueNow = numCustomerJourney.toString();

    document.getElementById("barPrivacyandDataCompliance").innerHTML = numPrivacyandDataCompliance + "%";
    document.getElementById("progressPrivacyandDataCompliance").style.width = numPrivacyandDataCompliance + "%";
    document.getElementById("progressPrivacyandDataCompliance").ariaValueNow = numPrivacyandDataCompliance.toString();

    document.getElementById("barCustomerLifetimeValue").innerHTML = numCustomerLifetimeValue + "%";
    document.getElementById("progressCustomerLifetimeValue").style.width = numCustomerLifetimeValue + "%";
    document.getElementById("progressCustomerLifetimeValue").ariaValueNow = numCustomerLifetimeValue.toString();

    document.getElementById("barSaaSMetrics").innerHTML = numSaaSMetrics + "%";
    document.getElementById("progressSaaSMetrics").style.width = numSaaSMetrics + "%";
    document.getElementById("progressSaaSMetrics").ariaValueNow = numSaaSMetrics.toString();
}

document.addEventListener("DOMContentLoaded", () => {
    fillBarGraphs();

    document.getElementById('URLuploadBtn').addEventListener('click', function() {
        const url = document.getElementById('url_article').value;
        fetchAndDisplayURLContent(url);
    });
});



