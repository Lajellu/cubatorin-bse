import logging
import requests
import ssl
import certifi

from rest_framework.response import Response
from rest_framework.decorators import api_view


# from pathlib import Path
# from django.http import JsonResponse
from bs4 import BeautifulSoup

from ai import ai

@api_view(['POST'])
def url_fetch_train(request):
    print("Received request to url_fetch_train")

    user_id = request.user.id
    data = request.data
    url = data['url']
    topic_id = data['topic_id']
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    url_fetch_response = requests.get(url, headers=headers)
    print(url_fetch_response)

    if url_fetch_response.status_code == 200:
        html_content = url_fetch_response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        body_text = soup.body.get_text(separator=' ', strip=True)
    else:
        print(f"Failed to retrieve data: {url_fetch_response.status_code}")
        return Response({'error': f"Failed to retrieve data: {url_fetch_response.status_code}"}, status=url_fetch_response.status_code)

    response = ai.train_model(user_id, topic_id, body_text, request.user)

    return Response(response)


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

