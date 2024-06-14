# This file does article summarization automatically using another request to ChatGPT (gpt-3.5-turbo)
# Writes to a JSONL file called "marketSizing.jsonl" with only two properties "prompt" and "completion"
# "prompt" should contain the article text, and "completion" should contain the summary generated
# Uploads the data to OpenAI API
# Uses the data to train a model
# TODO: Fix the printing of the model analysis
# TODO: The dropdown menu connects to the number of articles uploaded from each category in the bar graphs
# at the bottom of the advisor's page. Add all articles into the same model though.

from flask import Flask, request, jsonify
import os
import openai
import json
from openai import OpenAI
from flask_cors import CORS
import logging
from pathlib import Path
import time
import requests

# Set up Flask
app = Flask(__name__)
CORS(app)
logger = logging.getLogger("mypackage.mymodule")  # or __name__ for current module
logger.setLevel(logging.ERROR)


################ For index-advisee ##################
@app.route('/api/research', methods=['POST'])
def research():
    print("Received a request to /api/research")

    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    # TODO: Make industry and topic based on the drop-down menu
    industry = "parking"
    topic = "market sizing"

    # Use a pre-trained OpenAI API call to do research across the web for this information
    query = "Please do research for me given that my app is in the " + industry + "what is the usual geographical location, age, gender and income of user of this type of app?"
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "Please find correct market data across the web, based on other applications in the same industry. Data can be general (statistical) or specific to other existing applications. When referring to a general statistic, please provide the URL where the data was obtained. When referring to a specific application, list the application name and URL.  "

        },
        {
          "role": "user",
          "content": query
        }
      ],
      temperature=0.7,
      max_tokens=250,
      top_p=1
    )

    researchbyChatBot = response.choices[0].message.content
    print("Research is ready: ")
    print(researchbyChatBot)

    return jsonify(message=researchbyChatBot)


    
################ For index-advisor ##################
# Receive and handle the request to upload a new article
@app.route('/api/upload_summarize_train', methods=['POST'])
def upload_summarize_train():
    print("Received a request to /api/upload_summarize_train")
    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Extracting the text sent from the frontend
    data = request.json
    text_to_summarize = data['text']
    # print(f"Text to summarize: {text_to_summarize}")

    # Call OpenAI's API to summarize the text
    summary = openai_summarize_text(client, text_to_summarize)

    # print(f"Summary: {summary}")

    # Write to marketSizing.jsonl (adding to the data set)
    file_path = "topic_datasets_generated/marketSizing.jsonl"
    write_to_jsonl(file_path, text_to_summarize, summary)

    # Upload the data to be added as Training Data
    remote_openAI_file_id = upload_dataset(client, file_path)
    #########

    # Train the model
    fine_tuned_model = train_model(client, remote_openAI_file_id)

    # Check the fine-tuning status (Loop with a time delay)
    # Retrieve the fine-tuning job details
    status = client.fine_tuning.jobs.retrieve(fine_tuned_model.id).status
    if status not in ["succeeded", "failed"]:
        print(f"Job not in terminal status: {status}. Waiting.")
        while status not in ["succeeded", "failed"]:
            time.sleep(6)
            status = client.fine_tuning.jobs.retrieve(fine_tuned_model.id).status
            print(f"Status: {status}")

    if(status == "succeeded" ):
        print("--------- Finetune Job SUCCESS ---------")
        print(f"Finetune job {fine_tuned_model.id} finished with status: {status}")
        print("------------------")
        # Retrieve checkpoints
        checkpoints = retrieve_checkpoint_status(client, fine_tuned_model.id)
        # Analyze how well the model did
        # Print out the training loss, training token accuracy valid loss valid token accuracy
        retrieve_finetuning_metrics(client, fine_tuned_model.id)
    else:
        print(f"Finetune job {fine_tuned_model.id} finished with status: {status}")
        print("-------------------------")


    print("Checking other finetune jobs in the subscription.")
    all_trained_models = client.fine_tuning.jobs.list()
    print(f"Found {len(all_trained_models.data)} finetune jobs.")

    # Retrieve the finetuned model
    fine_tuned_model = all_trained_models.data[0].fine_tuned_model
    print("Fine tune model: ")
    print(fine_tuned_model)
    print("-------------------------")


    if fine_tuned_model is None:
        print("Failed to train model.")
    else:
        print("Fine_tuned_model existed")
        # TODO: Make these based on the user's profile
        industry = "parking"
        topic = "market sizing"
        msg_for_user_ret = query_trained_model(client, industry, topic, fine_tuned_model)
        return jsonify(message=msg_for_user_ret.content)

    return "Fine tune model didn't exist"

# TODO: Make this work with the latest fine tune job (so user can click on it without clicking upload first)
# Send the Cubatorin answer back to the frontend
@app.route('/test_me')
def test_me():
    print("---------- Testing the model just trained. ----------")
    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    # TODO: Make industry and topic based on the drop-down menu
    industry = "parking"
    topic = "market sizing"

    print("Checking other finetune jobs in the subscription.")
    all_trained_models = client.fine_tuning.jobs.list()
    # Uncomment this for information about all of the existing trained models, Training Parameters, and File Details
    # print(all_trained_models)
    # print(all_trained_models.data)
    print(f"-------- Found at least {len(all_trained_models.data)} finetune jobs: SUCCESS ----------")

    fine_tuned_model = all_trained_models.data[0].fine_tuned_model

    print(fine_tuned_model)

    if fine_tuned_model is None:
        print("Model not found")
        print("-------------------------")

    else:
        print("Fine_tuned_model existed")
        print("-------------------------")

        # query_trained_model returns the message
        chatCompletionMessage = query_trained_model(client, industry, topic, fine_tuned_model)
        chatCompletionMsgContent = chatCompletionMessage.content
        return jsonify(message=chatCompletionMsgContent)

    return "Model not found"

def openai_summarize_text(client, text_to_summarize):
    # TODO: Explicitly asked for 3 TODO's in prompt, potentially allow for changes to this number
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "Summarize content you are provided with for a university student in 3 sentences, being specific about the steps provided. Do not state that the article is about market sizing. Start and end the summary with specific steps. Break steps into bullet points instead of using commas for subtasks in each step. Start each step with a verb."

        },
        {
          "role": "user",
          "content": text_to_summarize
        }
      ],
      temperature=0.7,
      max_tokens=250,
      top_p=1
    )

    summaryByChatBot = response.choices[0].message.content
    print(summaryByChatBot)

    return summaryByChatBot


def write_to_jsonl(filename, article_text, summary):
    with open(filename, 'a') as f:  # Append to the jsonl file
        record = {
            "messages": [
                {
                    "role": "system",
                    "content": "Cubatorin is a factual chatbot helps new tech Entrepreneurs."
                },
                {
                    "role": "user",
                    "content": "I have just decided to build a new parking app, what steps do I take when performing market sizing?"
                },
                {
                    # TODO: Expert Knowledge: Get this from Rehber
                    "role": "assistant",
                    "content": summary
                }
            ]
        }

        f.write(json.dumps(record) + "\n")


def upload_dataset(client, local_file_path):
    try:
        # The 'file' parameter takes a path to the local file
        response = client.files.create(
            file=open(local_file_path, 'rb'),  # Open the file in binary read mode
            purpose="fine-tune",
        )
        print(f"--------- File uploaded with file ID: SUCCESS -------")
        print(response.id)
        return response.id
    except Exception as e:
        print(f"Failed to upload file: {e}")
        print("-------------------------")

        return None



def train_model(client, remote_openAI_file_id):
    try:
        fine_tuned_model = client.fine_tuning.jobs.create(
            model="gpt-3.5-turbo",
            training_file=remote_openAI_file_id,
        )

        # Consider changing the above to the commented part by ChatGPT
        # fine_tuned_model = client.fine_tuning.jobs.create(
        #    model="gpt-3.5-turbo",
        #    training_file=remote_openAI_file_id,
        #    compute_class="standard",  # You can adjust this based on your requirements
        #    n_epochs=4,  # Number of training epochs, adjust as necessary
        #    checkpoint_frequency=1  # Adjust frequency of checkpoints
        # )

        print("Model trained successfully with uploaded data")
        # print(fine_tuned_model)

        return fine_tuned_model  # Retrieve the name of the fine-tuned model
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        print("-------------------------")
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        print("-------------------------")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        print(e.response.text)  # Printing the detailed error message
        print("-------------------------")
        return None

def query_trained_model(client, industry, topic, fine_tuned_model):
    query = "I have just decided to build a new" + industry + "app, what steps do I take when performing" + topic + "?"
    completion = client.chat.completions.create(
      model = fine_tuned_model,
      messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
       ]
    )
    print("-------------------------")
    print("Test the query")

    msg_for_user = completion.choices[0].message
    print("Content: " + msg_for_user.content)
    print("Role: " + msg_for_user.role)
    return msg_for_user


def retrieve_checkpoint_status(client, fine_tuned_model_id):
    try:
        fine_tune_details = client.fine_tuning.jobs.retrieve(fine_tuned_model_id)
        print("------ Retrieved checkpoint: SUCCESS --------")
        # Uncomment this for information about the model, Training Parameters, and File Details
        # print(fine_tune_details)
        return fine_tune_details
    except Exception as e:
        print(f"Failed to retrieve checkpoints: {e}")
        print("-------------------------")
        return None


def retrieve_finetuning_metrics(client, fine_tuned_model_id):
    try:
        print("-------------------------")
        print("---- Analyze the model: Print out the training loss, training token accuracy, validation loss, and validation token accuracy -----")

        # Retrieve events for the fine-tuning job
        events = client.fine_tuning.jobs.list_events(fine_tuned_model_id).data

        if events:
            # Find the latest event with metrics
            for event in reversed(events):
                if event.type == 'metrics':
                    data = event.data
                    print(f"Training Loss: {data.get('train_loss')}")
                    print(f"Training Token Accuracy: {data.get('train_mean_token_accuracy')}")
                    print(f"Validation Loss: {data.get('valid_loss')}")
                    print(f"Validation Token Accuracy: {data.get('valid_mean_token_accuracy')}")
                    print(f"Full Validation Loss: {data.get('full_valid_loss')}")
                    print(f"Full Validation Token Accuracy: {data.get('full_valid_mean_token_accuracy')}")
                    print("-------------------------")

                    break
        else:
            print("No events found with metrics.")
            print("-------------------------")


        return events
    except Exception as e:
        print(f"Failed to retrieve fine-tuning job details: {e}")
        print("-------------------------")

        return None


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)

