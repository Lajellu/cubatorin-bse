# WORKS: This file can read the file uploaded in advisorUploadUI.html
# TODO: The file should now be sent to the ChatGPT_summarize file so that it can be added to
#       the training data set as its "completion" column value

import os
from pyscript import when
from datetime import datetime
from js import FileReader, document
from js import JSON


print("Hello World")
target_div = Element("printSpace")
target_div.element.innerText = "test"

@when('click', '#uploadBtn')
def handle_upload():
    target_div = Element("printSpace")
    target_div.element.innerText = "Contents of the file just uploaded:"
    file_input = Element('file').element  # Access the file input element
    fileList = file_input.files

    # Read each first file uploaded in order
    if fileList.length > 0:
        for f in fileList:
            # Print the file information to the PyScript console
            print("File Name: " + f.name)
            print("File Size: " + str(f.size))
            print("File Size: " + str(f.size / 1024), "KB")

            # Assuming 'f' is your file object
            last_modified_timestamp = f.lastModified
            # Convert from milliseconds to seconds
            last_modified_date = datetime.fromtimestamp(last_modified_timestamp / 1000)
            print(last_modified_date.strftime("%Y-%m-%d %H:%M:%S"))
            print("Last Modified: " + str(last_modified_date))

            # Prepare to read the contents file
            reader = FileReader.new()

            # TODO LATER: Add validation of the text, and fix quotes
            #           : Manually replaced all double quotes ' with single quotes '. Use Regex for this


            def onload(event):
                # This function is called when the FileReader has read the file
                file_contents = event.target.result
                document.getElementById("fileContents").innerText = file_contents
                data = JSON.stringify({'text': file_contents})
                headers = {'Content-Type': 'application/json'}

                # Using JavaScript fetch API to send the file content to your backend
                fetch('http://127.0.0.1:5000/api/summarize', {
                    "method": "POST",
                    'headers': headers,
                    'body': data
                })


                def on_success(response):
                    # Assuming your backend responds with a JSON containing the summary
                    js_response = response.json()
                    js_response.then(lambda data: print(data['summary']))

                def on_fail(error):
                    print("Failed to send data to backend:", error)

                promise.then(on_success, on_fail)

            reader.onload = onload
            reader.readAsText(f)

