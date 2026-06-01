from django.contrib import admin
from .models import InterviewQuestion, PracticeSession

@admin.register(InterviewQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'difficulty', 'role_tag']
    list_filter = ['category', 'difficulty']

admin.site.register(PracticeSession)
