import time

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q

from advisor.models import Topic
from ai import ai

from .models import Advisee

def regenerate_advisee_topic_instructions(advisee_id):
    print("(thread started) Regnerating advisee topic instructions [advisee_id " + str(advisee_id) + "]")
    
    advisee = Advisee.objects.get(id=advisee_id)
    topics = Topic.objects.filter(active=True).order_by("order")

    for topic in topics: 
        # systemPrompt = "Please find correct market data across the web, based on other applications in the same industry. Data can be general (statistical) or specific to other existing applications. When referring to a general statistic, please provide the URL where the data was obtained. When referring to a specific application, list the application name and URL.  "
        systemPrompt = "Provide step-by-step instructions for how to perform " + topic.name + " including any required calculations and legal considerations. Respond in under 200 words and a maximum of 4 steps."
        userPrompt = "I'm building an app in the " + advisee.industry + " industry. Provide and explain the detailed steps for how to perform " + topic.name
        
        print("----------------------------------")
        print ("On topic " + topic.name)
        print ("PROMPT: " + userPrompt)
        print ("INSTRUCTIONS:")

        result = ai.prompt(systemPrompt, userPrompt)
        print (result)

        advisee.set_topic_instruction(topic.id, result)
    
    advisee.save()

    print("(thread finished) Regnerating advisee topic instructions [advisee_id " + str(advisee_id) + "]")

def regenerate_all_advisee_topic_instructions_and_notify_by_email(notify_email):
    # get all advisees who have an industry set
    all_advisees = Advisee.objects.filter(Q(industry__isnull=False) & ~Q(industry=''))
    
    for advisee in all_advisees:
        regenerate_advisee_topic_instructions(advisee.id)

    email = EmailMessage(
        "Regenerated all advisees' topic instructions using new AI model",
        "Regenerated all advisees' topic instructions using new AI model",
        settings.EMAIL_HOST_USER,
        [notify_email])
    email.content_subtype = 'html'
    email.send(fail_silently=False)