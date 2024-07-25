from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.conf import settings

from advisee.models import Advisee
from .forms import AdvisorRegistrationForm
from .forms import AdvisorLoginForm
from .models import Advisor, Article, Topic
from .decorators import advisor_login_required


def article_feedback(request, id, feedback):

    try:
        article = Article.objects.get(id=id)

        if (article.status != "FINETUNE-SUCCEEDED"):
            message_header = "Can't provide feedback for this article"
            message_body = f"The article must be in 'FINETUNE-SUCCEEDED' state before you can provide feedback. Currently it's in the '{article.status}' state"
            message_class = "alert-danger"
        else:
            if (feedback == "accept"):
                article.status = "ACCEPTED"
                article.save()

                message_header = "Thank you for accepting this article"
                message_body = "From now on, the AI will use this article to help Advisees."
                message_class = "alert-success"
            elif (feedback == "reject"):
                article.status = "REJECTED"
                article.save()

                message_header = "Thank you for rejecting this article"
                message_body = "The AI will not use this article to help Advisees."
                message_class = "alert-success"
            else:
                message_header = "Incorrect Feedback"
                message_body = f"The feedback can only be 'accept' or 'reject', not '{feedback}'"
                message_class = "alert-danger"

    except Article.DoesNotExist as e:
        message_header = "Can't find article"
        message_body = "The article ID provided in the link is incorrect"
        message_class = "alert-danger"

    return render(request, 'advisor/article-feedback.html', {
        'message_header': message_header,
        'message_body': message_body, 
        'message_class': message_class
    })

@advisor_login_required
def advisee(request, id):
    advisor = Advisor.objects.select_related('user').get(user_id=request.user.id)
    advisee = Advisee.objects.select_related('user').get(id=id)

    return render(request, 'advisor/advisee.html', {
        'advisee': advisee
    })

@advisor_login_required
def advisees(request):
    advisor = Advisor.objects.select_related('user').get(user_id=request.user.id)
    advisees = advisor.advisee_set.all()

    return render(request, 'advisor/advisees.html', {
        'advisees': advisees
    })


@advisor_login_required
def dashboard(request):
    advisor = Advisor.objects.get(user_id=request.user.id)
    num_advisees = Advisee.objects.filter(advisor=advisor).count()
    num_articles = Article.objects.filter(status='SUCCEEDED').count()
    num_articles_by_advisor = Article.objects.filter(advisor=advisor, status='SUCCEEDED').count()
    topics = Topic.objects.all()
    
    num_articles_per_topic = Topic.objects.annotate(
        num_articles=Count('article', filter=Q(article__status='SUCCEEDED'))
        ).values('id','name','num_articles')
    pprint(list(num_articles_per_topic))
    
    perc_articles_per_topic = []
    for row in num_articles_per_topic:
        perc_articles_per_topic.append({
            'topic_name':row['name'], 
            'topic_name_no_space': row['name'].replace(" ", ""),
            'perc_complete':int(row['num_articles']/30*100)})
    pprint(perc_articles_per_topic)

    return render(request, 'advisor/dashboard.html', {
        'user':request.user, 
        'num_advisees':num_advisees,
        'num_articles':num_articles,
        'num_articles_by_advisor': num_articles_by_advisor, 
        'topics':topics,
        'perc_articles_per_topic':perc_articles_per_topic,
        })

def index(request):
    return render(request, 'advisor/index.html')

def logout(request):
    logoutUser(request)
    return redirect('/advisor')

def login(request):
    form_errors = None;

    if request.method == 'POST':
        form = AdvisorLoginForm(request, request.POST)
        if form.is_valid():
            loginUser(request, form.get_user())
            return redirect('/advisor/dashboard')
        else:
            form_errors = form.errors.get("__all__")
    else:
        form = AdvisorLoginForm()

    return render(request, 'advisor/login.html', {'form':form, 'form_errors':form_errors})

def register(request):
    if request.method == 'POST':
        pprint(request.POST)
        form = AdvisorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
            
                    advisor = Advisor.objects.create(user=user)
            except Exception as e:
                print(f"Exception: {e}")
            else:
                # username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user.username + '. You can now login!')

            return redirect('/advisor/login/')
    else:
        form = AdvisorRegistrationForm()
    
    print(form.errors)
    return render(request, 'advisor/register.html', {'form':form})
