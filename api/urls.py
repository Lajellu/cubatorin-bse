from django.urls import path
from . import views

urlpatterns = [
    path('file_upload_train/', views.file_upload_train),
    path('research/', views.research),
    path('url_fetch_train/', views.url_fetch_train),
    path('raw_text_upload_train/', views.raw_text_upload_train),
    path('mark_advisee_topic_instruction_read/', views.mark_advisee_topic_instruction_read)
]