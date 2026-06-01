from django.contrib import admin
from .models import Job, Application, SavedJob

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'job_type', 'created_at']
    list_filter = ['status', 'job_type', 'experience_level']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'match_score', 'applied_at']
    list_filter = ['status']

admin.site.register(SavedJob)
