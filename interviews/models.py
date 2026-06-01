from django.db import models
from accounts.models import JobSeekerProfile, CompanyProfile


class InterviewQuestion(models.Model):
    CATEGORY = (
        ('behavioral','Behavioral'),
        ('technical','Technical'),
        ('situational','Situational'),
        ('hr','HR & Culture'),
        ('leadership','Leadership'),
    )
    DIFFICULTY = (('easy','Easy'),('medium','Medium'),('hard','Hard'))

    category = models.CharField(max_length=20, choices=CATEGORY)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='medium')
    role_tag = models.CharField(max_length=100, blank=True, help_text='e.g. Software Engineer, Marketing')
    question = models.TextField()
    sample_answer = models.TextField()
    tips = models.TextField(blank=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='interview_questions', help_text='Leave blank for global questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:80]

    class Meta:
        ordering = ['category', 'difficulty']


class PracticeSession(models.Model):
    seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='practice_sessions')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField()
    score = models.PositiveIntegerField(default=0)  # 0-100
    feedback = models.TextField(blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seeker.full_name} - {self.question.category}"

    class Meta:
        ordering = ['-attempted_at']
