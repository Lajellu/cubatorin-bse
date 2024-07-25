import os
import openai
import json
import logging
import time
import requests
import ssl
import certifi
import traceback

from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from pprint import pprint
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from advisor.models import Advisor, Topic, Article

load_dotenv()

@api_view(['POST'])
def file_upload_train(request):
    print("Received a request to /api/file_upload_train")
    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Extracting the text sent from the frontend
    data = request.data
    text_to_summarize = data['text']
    # print(f"Text to summarize: {text_to_summarize}")

    # Create article in DB
    advisor = Advisor.objects.get(user_id=request.user.id)
    topic = Topic.objects.get(id=data['topic_id'])
    article = Article(
        name="Article Name",
        advisor=advisor,
        topic=topic,
        body=text_to_summarize
    )
    article.save()

    # Summarize text with OpenAI
    try:
        article.status = "SUMMARIZE-PROCESSING"
        article.save()

        summary = openai_summarize_text(client, text_to_summarize)

        article.summary = summary
        article.save()
    except Exception as e:
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "SUMMARIZE-FAILED"
        article.failure_reason = error_str
        article.save()

        return Response(str(e))

    # TODO: generate db.jsonl from db.seed.jsonl + articles in DB
    # Write to db.jsonl (adding to the data set)
    file_path = "articles_and_summaries/db.jsonl"
    write_to_jsonl(file_path, text_to_summarize, summary)

    # Upload the data to be added as Training Data
    try:
        article.status = "UPLOADDATA-PROCESSING"
        article.save()

        remote_openAI_file_id = upload_dataset(client, file_path)
    except Exception as e: 
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "UPLOADDATA-FAILED"
        article.failure_reason = error_str
        article.save()

        return Response(str(e))

    # Fine-tune the model
    try:
        article.status = "FINETUNE-PROCESSING"
        article.save()

        # Create fine-tuning job on OpenAI
        fine_tuned_model = finetune_model(client, remote_openAI_file_id)

        # Check the fine-tuning job status (Loop with a time delay)
        status = ""
        while status not in ["succeeded", "failed"]:
            status = client.fine_tuning.jobs.retrieve(fine_tuned_model.id).status
            time.sleep(10)
            print(f"Status: {status}")

        # If fine-tuning failed, raise an exception
        if (status == "failed"):
            print(f"Finetune job {fine_tuned_model.id} finished with status: {status}")
            print("-------------------------")

            raise Exception(f"Finetune job {fine_tuned_model.id} finished with status: {status}")

        # fine-tuning has successed
        # Retrieve the fine-tuning job details
        print("--------- Finetune Job SUCCESS ---------")
        print(f"Finetune job {fine_tuned_model.id} finished with status: {status}")
        print("------------------")
        
        # Retrieve checkpoints
        finetune_checkpoints = retrieve_checkpoint_status(client, fine_tuned_model.id)
        
        # Analyze how well the model did
        # Print out the training loss, training token accuracy valid loss valid token accuracy
        finetune_metrics = retrieve_finetuning_metrics(client, fine_tuned_model.id)

        print("Checking other finetune jobs in the subscription.")
        all_trained_models = client.fine_tuning.jobs.list()
        print(f"Found {len(all_trained_models.data)} finetune jobs.")
        
        article.status = "FINETUNE-SUCCEEDED"
        article.finetune_checkpoints = finetune_checkpoints
        article.finetune_metrics = finetune_metrics
        article.save()

    except Exception as e:
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "FINETUNE-FAILED"
        article.failure_reason = error_str
        article.save()

        return Response(str(e))

    # Test the model
    try:
        # Retrieve the finetuned model
        fine_tuned_model = all_trained_models.data[0].fine_tuned_model
        print("Fine tune model: ")
        print(fine_tuned_model)
        print("-------------------------")

        # If model retrieval failed, raise an exception
        if fine_tuned_model is None:
            print("Cannot retrieve fine-tuned model")
            raise Exception("Fine-tuning succeeded, but cannot retrieve fine-tuned model")
        

        # Model retrieval succeeded
        # Test the model by querying it
        # TODO: how to set industry and topic dynamically so it makes sense? 
        industry = "parking"
        test_query = "I have just decided to build a new " + industry + " app. What steps do I take when performing " + topic.name + "?"
        test_result = query_trained_model(client, fine_tuned_model, test_query).content

        article.test_query = test_query
        article.test_result = test_result
        article.save()

        # Email user to notify of fine-tuning completion, sent test results and ask for feedback
        accept_url = settings.PROTOCOL + settings.DOMAIN_NAME + f"/advisor/article/{article.id}/feedback/accept"
        reject_url = settings.PROTOCOL + settings.DOMAIN_NAME + f"/advisor/article/{article.id}/feedback/reject"
        email = EmailMessage(
            'AI trained successfully with your article', 
            f"Here's the test results: <br><br> \
                {test_result}<br><br> \
                Did this improve the AI? \
                <a href='{accept_url}'>yes</a> \
                <a href='{reject_url}'>no</a>", 
            settings.EMAIL_HOST_USER, 
            [request.user.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        return Response({"message":test_result})


    except Exception as e:
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "FINETUNE-FAILED"
        article.failure_reason = error_str
        article.save()

        return Response(str(e))


@api_view(['POST'])
def research(request):
    print("Received a request to /api/research")

    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    # TODO: Make the industry based on the entrepreneur's profile and topic based on frontend-advisee side "startup step"
    data = request.data
    industry = data['industry']
    topic = data['topic']

    # Use a pre-trained OpenAI API call to do research across the web for this information
    # query = "Please do research for me given that my app is in the " + industry + ". what is the usual geographical location, age, gender and income of user of this type of app?"
    query = "I'm building an app in the " + industry + "industry. Do some " + topic + " research for me"

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

    return Response({"message":researchbyChatBot})

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
        # The 'file' parameter takes file pointer
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

        raise e

def finetune_model(client, remote_openAI_file_id):
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

        print("Fine-tuning job created successfully")
        # print(fine_tuned_model)

        return fine_tuned_model  # Retrieve the name of the fine-tuned model

    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        print("-------------------------")

        raise e
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        print("-------------------------")

        raise e
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        print(e.response.text)  # Printing the detailed error message
        print("-------------------------")

        raise e

def query_trained_model(client, fine_tuned_model, query):
    
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
    fine_tune_details = client.fine_tuning.jobs.retrieve(fine_tuned_model_id)
    
    print("------ Retrieved checkpoint: SUCCESS --------")
    # Uncomment this for information about the model, Training Parameters, and File Details
    # print(fine_tune_details)

    return fine_tune_details

def retrieve_finetuning_metrics(client, fine_tuned_model_id):
    print("-------------------------")
    print("---- Analyze the model: Print out the training loss, training token accuracy, validation loss, and validation token accuracy -----")

    # Retrieve events for the fine-tuning job
    events = client.fine_tuning.jobs.list_events(fine_tuned_model_id).data
    metrics = ""

    if events:
        # Find the latest event with metrics
        for event in reversed(events):
            if event.type == 'metrics':
                data = event.data

                metrics += f"Training Loss: {data.get('train_loss')}\n"
                metrics += f"Training Token Accuracy: {data.get('train_mean_token_accuracy')}\n"
                metrics += f"Validation Loss: {data.get('valid_loss')}\n"
                metrics += f"Validation Token Accuracy: {data.get('valid_mean_token_accuracy')}\n"
                metrics += f"Full Validation Loss: {data.get('full_valid_loss')}\n"
                metrics += f"Full Validation Token Accuracy: {data.get('full_valid_mean_token_accuracy')}\n"
                metrics += "-------------------------"

                print(metrics)

                break
    else:
        metrics += "No events found with metrics."
        metrics += "-------------------------"

        print(metrics)

    return metrics
