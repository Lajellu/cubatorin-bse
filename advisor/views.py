from pprint import pprint

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from django.conf import settings
from django.urls import reverse

from advisee.models import Advisee
from .forms import AdvisorRegistrationForm
from .forms import AdvisorLoginForm
from .models import Advisor, Article, Topic, Mail
from .decorators import advisor_login_required

@advisor_login_required
def message_send (request, advisee_id):
    advisor = Advisor.objects.get(user=request.user)
    advisee = Advisee.objects.get(id=advisee_id)

    message_body = request.POST['reply-textarea'].strip()

    if (message_body != ""):
        mail = Mail(
            sender = advisor.user,
            receiver = advisee.user,
            body = message_body
        )
        mail.save()
    
    return redirect(reverse("advisor:message_advisee", kwargs={"advisee_id":advisee_id}))

@advisor_login_required
def message_advisee (request, advisee_id):
    advisor = Advisor.objects.get(user=request.user)
    advisee = Advisee.objects.get(id=advisee_id)

    all_mails_reults = Mail.objects.filter(
        (Q(sender=advisor.user.id) &  Q(receiver=advisee.user.id)) | (Q(sender=advisee.user.id) & Q(receiver=advisor.user.id))
    ).order_by("sent_at")
        
    all_mails = []
    for mail in all_mails_reults:
        all_mails.append({
            'sender': f"{mail.sender.first_name} {mail.sender.last_name}",
            'receiver': f"{mail.receiver.first_name} {mail.receiver.last_name}",
            'sent_at': mail.sent_at.strftime("%B %d '%y - %I:%M %p"),
            'unread_class': 'fa-circle' if mail.unread and mail.receiver == advisor.user else '',
            'body': mail.body.replace("\n", "<br/>")
        })

        if mail.unread and mail.receiver == advisor.user:
            mail.unread = False
            mail.save()


    return render(request, "advisor/message/advisee.html", {
        'advisee': advisee,
        'all_mails': all_mails
    })


@advisor_login_required
def message_inbox (request):
    advisor = Advisor.objects.get(user=request.user)
    advisees = Advisee.objects.filter(advisor=advisor)

    latest_mails = []
    for advisee in advisees:
        latest_mail = Mail.objects.filter(Q(sender=advisee.user) | Q(receiver=advisee.user)).order_by("-sent_at")[:1].first()

        sender = latest_mail.sender
        receiver = latest_mail.receiver
        unread = latest_mail.unread
        body = latest_mail.body
        sent_at = latest_mail.sent_at

        latest_mails.append({
            'advisee': advisee,
            'unread_class': 'fa-circle' if unread and receiver == advisor.user else '',
            'correspondent': receiver if sender == advisor.user else sender,
            'snippet': body[:50] + ('...' if len(body) > 50 else ''),
            'datetime': sent_at.strftime("%B %d '%y - %I:%M %p")
        })

    return render(request, "advisor/message/inbox.html", {
        'latest_mails': latest_mails
    })

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
def advisee (request, id):
    advisor = Advisor.objects.select_related('user').get(user_id=request.user.id)
    advisee = Advisee.objects.select_related('user').get(id=id)
    topics = Topic.objects.filter(active=True).order_by("order")

    topics_data = []
    for topic in topics: 
        topics_data.append({
            'id': topic.id,
            'name': topic.name,
            'text': advisee.get_topic_text(topic.id)
        })

    return render(request, 'advisor/advisee.html', {
        'advisee': advisee,
        'topics_data': topics_data
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
    num_articles = Article.objects.filter(status='ACCEPTED').count()
    num_articles_by_advisor = Article.objects.filter(advisor=advisor, status='ACCEPTED').count()
    topics = Topic.objects.all().filter(active=True).order_by("order")
    
    num_articles_per_topic = Topic.objects.annotate(
        num_articles=Count('article', filter=Q(article__status='ACCEPTED'))
        ).values('id','name','num_articles').order_by("order")
    
    perc_articles_per_topic = []
    for row in num_articles_per_topic:
        perc_articles_per_topic.append({
            'topic_name':row['name'], 
            'topic_name_no_space': row['name'].replace(" ", ""),
            'perc_complete':int(row['num_articles']/30*100)})

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
