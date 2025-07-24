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