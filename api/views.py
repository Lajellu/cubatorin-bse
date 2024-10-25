import threading
import logging
import requests
import ssl
import certifi

from rest_framework.response import Response
from rest_framework.decorators import api_view

from bs4 import BeautifulSoup

from ai import ai

from advisee.models import Advisee

from playwright.sync_api import sync_playwright

@api_view(['POST'])
def url_fetch_train(request):
    print("Received request to url_fetch_train")

    user_id = request.user.id
    data = request.data
    url = data['url']
    topic_id = data['topic_id']
    
    body_text = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            response = page.goto(url)

            if response and response.status == 200:
                print(f"Successfully fetched the page: {url}")

                # Wait for page to load
                page.wait_for_timeout(5000)

                html_content = page.content()
                # print(html_content)
                # TODO: Merge the Beautiful soup code here (Expected a `Response`, `HttpResponse` or `StreamingHttpResponse` to be returned from the view, but received a `<class 'NoneType'>`)
                soup = BeautifulSoup(html_content, "html.parser")

                # Remove elements that are not visible or relevant
                for element in soup(['script', 'style', 'noscript', 'iframe', 'header', 'footer', 'aside', '[hidden]']):
                    element.decompose()  # Completely remove these elements from the soup

                # Optionally remove elements by class or ID related to ads, popups, etc.
                for element in soup.find_all(True, {'class': ['ad', 'popup', 'modal', 'banner'], 'id': ['ad', 'popup', 'modal', 'banner']}):
                    element.decompose()

                body_text = soup.body.get_text(separator=' ', strip=True)
                print(body_text)

        except Exception as e:
            print(f"Error caught: An error occurred: {e}")
            return Response({'error': f"Failed to retrieve data: {e}"}, status=500)

        finally:
            browser.close()


    def background_task():
        response = ai.train_model(user_id, topic_id, body_text, request.user)

    thread = threading.Thread(target=background_task)
    thread.start()

    return Response({"message" : "Success parsing body text from the requested URL:" + url})


@api_view(['POST'])
def raw_text_upload_train(request):
    print("Received a request to /api/file_upload_train")
    data = request.data
    body_text = data['text']
    print(f"Text to summarize: {body_text}")

    user_id = request.user.id
    topic_id = data['topic_id']
    
    
    # Train the AI using the raw text entered (on a new thread)
    def background_task():
        response = ai.train_model(user_id, topic_id, body_text, request.user)

    thread = threading.Thread(target=background_task)
    thread.start()

    return Response({"message" : "Success reading raw text entered"})


@api_view(['POST'])
def file_upload_train(request):
    print("Received a request to /api/file_upload_train")

    # Extracting the text sent from the frontend
    data = request.data
    text_to_summarize = data['text']
    # print(f"Text to summarize: {text_to_summarize}")

    user_id = request.user.id
    topic_id = data['topic_id']
    response = ai.train_model(user_id, topic_id, text_to_summarize, request.user)

    return Response(response)


@api_view(['POST'])
def research(request):
    print("Received a request to /api/research")

    data = request.data
    industry = data['industry']
    topic = data['topic']

    # Use a pre-trained OpenAI API call to do research across the web for this information
    # query = "Please do research for me given that my app is in the " + industry + ". what is the usual geographical location, age, gender and income of user of this type of app?"
    userPrompt = "I'm building an app in the " + industry + "industry. Do some " + topic + " research for me"
    systemPrompt = "Please find correct market data across the web, based on other applications in the same industry. Data can be general (statistical) or specific to other existing applications. When referring to a general statistic, please provide the URL where the data was obtained. When referring to a specific application, list the application name and URL.  "

    researchbyChatBot = ai.prompt(systemPrompt, userPrompt)

    return Response({"message":researchbyChatBot})

@api_view(['POST'])
def mark_advisee_topic_instruction_read(request):
    data = request.data
    topic_id = data["topic_id"]
    advisee = Advisee.objects.get(user_id=request.user.id)

    advisee.mark_topic_instruction_read(topic_id)

    advisee.save()

    return Response({"message":str(advisee) + " topic instruction for topic_id " + topic_id + " set to read"})

