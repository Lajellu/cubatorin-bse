import traceback

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from advisor.models import Advisor, Topic, Article, Mail
from advisee.models import Advisee

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('Seeding Database...'))

        try:
            self.stdout.write('  Creating Admin user...')
            self.create_admin_user()
            self.stdout.write(self.style.SUCCESS('  OK'))

            self.stdout.write('  Creating Advisors...')
            self.create_advisors()
            self.stdout.write(self.style.SUCCESS('  OK'))

            self.stdout.write('  Creating Topics...')
            self.create_topics()
            self.stdout.write(self.style.SUCCESS('  OK'))

            self.stdout.write('  Creating Advisees...')
            self.create_advisees()
            self.stdout.write(self.style.SUCCESS('  OK'))

            self.stdout.write('  Creating Mails...')
            self.create_mails()
            self.stdout.write(self.style.SUCCESS('  OK'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
            traceback.print_exc()


    def create_admin_user(self):
        su = User.objects.create_superuser(
        username='admin', 
        email='admin@mailinator.com', 
        password='admin', 
        first_name="Laily", 
        last_name="Ajellu",
        last_login=timezone.now())

    def create_advisors(self):
        u1 = User.objects.create_user(
            username="advisor1",
            email='advisor1@mailinator.com', 
            is_active=1, 
            password="advisor1", 
            first_name="advisor", 
            last_name="1", 
            last_login=timezone.now())
        a1 = Advisor(user=u1)
        a1.save()

        u2 = User.objects.create_user(
            username="advisor2",
            email='advisor2@mailinator.com', 
            is_active=1, 
            password="advisor2", 
            first_name="advisor", 
            last_name="2", 
            last_login=timezone.now())
        a2 = Advisor(user=u2)
        a2.save()
    
    def create_topics(self):
        Topic.objects.create(name='Market Sizing', order=1)
        Topic.objects.create(name='Product Market Fit', order=2)
        Topic.objects.create(name='Valuation', order=3)
        Topic.objects.create(name='Capitalization', order=4)
        Topic.objects.create(name='Competitive Analysis', order=5)
        Topic.objects.create(name='Content Marketing', order=6)
        Topic.objects.create(name='Networking', order=7)
        Topic.objects.create(name='Customer Journey', order=8)
        Topic.objects.create(name='Privacy and Data Compliance', order=9)
        Topic.objects.create(name='Customer Lifetime Value', order=10)
        Topic.objects.create(name='SaaS Metrics', order=11)

    def create_advisees(self):
        advisor = Advisor.objects.get(id=1)
        topics = Topic.objects.filter(active=True).order_by("order")
        
        ### Advisee 1
        u1 = User.objects.create_user(
            username="advisee1",
            email='advisee1@mailinator.com', 
            is_active=1, 
            password="advisee1", 
            first_name="advisee", 
            last_name="1",
            last_login=timezone.now()
            )
        
        a1 = Advisee(
            user=u1, 
            advisor=advisor,
            industry = "ad1 industry"
            )
        for topic in topics:
            a1.set_topic_text(topic.id, topic.name + " topic text")
            a1.set_topic_instruction(topic.id, topic.name + " topic instructions", True)

        a1.save()

        ### Advisee 2
        u2 = User.objects.create_user(
            username="advisee2",
            email='advisee2@mailinator.com', 
            is_active=1, 
            password="advisee2", 
            first_name="advisee", 
            last_name="2", 
            last_login=timezone.now()
            )

        a2 = Advisee(
            user=u2, 
            advisor=advisor,
            industry = "ad2 industry"
            )
        for topic in topics:
            a2.set_topic_text(topic.id, topic.name + " topic text")
            a2.set_topic_instruction(topic.id, topic.name + " topic instructions", True)

        a2.save()
    
    def create_mails(self):
        advisor1 = Advisor.objects.get(id=1).user
        advisee1 = Advisee.objects.get(id=1).user
        advisee2 = Advisee.objects.get(id=2).user

        Mail(sender=advisor1, receiver=advisee1, body="Hi there").save()
        Mail(sender=advisee1, receiver=advisor1, body="Hi back").save()

        Mail(sender=advisee2, receiver=advisor1, body="Hi my advisor").save()
        Mail(sender=advisor1, receiver=advisee2, body="Hi my advisee").save()