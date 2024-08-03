from django.contrib.auth.models import User
from advisor.models import Mail  # Import your Mail model

def unread_messages(request):
    if request.user.is_authenticated:
        # Query the database for unread messages for the logged-in user
        unread_count = Mail.objects.filter(receiver=request.user, unread=True).count()
    else:
        unread_count = 0

    return {'unread_messages_count': unread_count}
