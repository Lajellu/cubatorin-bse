from django.contrib import admin
from .models import Topic, Advisor

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ('id',)

class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    ordering = ('id',)


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Advisor, AdvisorAdmin)