import os
import openai
import traceback
import shutil
import json
import time

from dotenv import load_dotenv
from openai import OpenAI
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage

from advisor.models import Advisor, Topic, Article

load_dotenv()

def prompt(systemPrompt, userPrompt):
    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": systemPrompt
        },
        {
          "role": "user",
          "content": userPrompt
        }
      ],
      temperature=0.7,
      max_tokens=500,
      top_p=1
    )

    responseByChatBot = response.choices[0].message.content

    return responseByChatBot


def train_model(user_id, topic_id, text_to_summarize, user):
    print("About to train the model")
    
    # Ensure your OPENAI_API_KEY environment variable is set
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Create article in DB
    advisor = Advisor.objects.get(user_id=user_id)
    topic = Topic.objects.get(id=topic_id)
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

        return error_str

    # Generate db.jsonl by copying db.seed.jsonl and
    # appending all ACCEPTED articles and the current article being processed
    try:
        all_accepted_articles_and_current_article = Article.objects.filter(Q(status='ACCEPTED') | Q(id=article.id))

        db_dir = "articles_and_summaries/"
        db_seed_jsonl_path = db_dir + 'db.seed.jsonl'
        db_jsonl_path = db_dir + 'db.jsonl'

        generate_articles_and_summaries_jsonl(db_jsonl_path, db_seed_jsonl_path, all_accepted_articles_and_current_article)
    except Exception as e:
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "SUMMARIZE-FAILED"
        article.failure_reason = error_str
        article.save()

        return error_str

    # Upload the data to be added as Training Data
    try:
        article.status = "UPLOADDATA-PROCESSING"
        article.save()

        remote_openAI_file_id = upload_dataset(client, db_jsonl_path)
    except Exception as e:
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "UPLOADDATA-FAILED"
        article.failure_reason = error_str
        article.save()

        return error_str

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

        # fine-tuning has succeeded
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

        return error_str

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

        # Email user to notify of fine-tuning completion, send test results and ask for feedback
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
            [user.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        return test_result


    except Exception as e:
        error_str = str(e) + "\n" + "".join(traceback.format_tb(e.__traceback__))

        article.status = "FINETUNE-FAILED"
        article.failure_reason = error_str
        article.save()

        return error_str

def openai_summarize_text(client, text_to_summarize):
    # TODO: Explicitly asked for 3 TODO's in prompt, potentially allow for changes to this number
    response = client.chat.completions.create(
      model="gpt-4",
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
      max_tokens=500,
      top_p=1
    )

    summaryByChatBot = response.choices[0].message.content
    print(summaryByChatBot)

    return summaryByChatBot

def generate_articles_and_summaries_jsonl(db_jsonl_path, db_seed_jsonl_path, articles):
    # copy db.seed.jsonl and replace db.jsonl if it already exists
    shutil.copy(db_seed_jsonl_path, db_jsonl_path)

    # open db.jsonl for appending
    db_jsonl_file = open(db_jsonl_path, 'a')

    # TODO: connect this with the variables in the profile of the advisee
    # loop through articles and append summary records to db.jsonl
    for article in articles:
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
                    "content": article.summary
                }
            ]
        }

        db_jsonl_file.write(json.dumps(record) + "\n")


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
            model = "gpt-4",
            training_file = remote_openAI_file_id
        )

        """
        # TODO: Potentially play with these hyperparameters. This is a argument for create()
        hyperparameters = {
            "n_epochs": 2,
            "batch_size": 2,
            "checkpoint_frequency": 1,
            "compute_class": "standard",
            "validation_file": "replace_this"
        }
        """

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