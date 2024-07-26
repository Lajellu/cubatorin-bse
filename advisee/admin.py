from django.contrib import admin
from .models import Advisee

class AdviseeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'industry')
    ordering = ('id',)

# Register your models here.
admin.site.register(Advisee, AdviseeAdmin)