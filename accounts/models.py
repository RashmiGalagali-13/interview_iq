from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (('jobseeker', 'Job Seeker'), ('company', 'Company'), ('admin', 'Admin'))
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='jobseeker')
    email = models.EmailField(unique=True)

    def is_company(self):
        return self.user_type == 'company'

    def is_jobseeker(self):
        return self.user_type == 'jobseeker'

    def is_admin_user(self):
        return self.user_type == 'admin' or self.is_superuser


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=200, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    desired_role = models.CharField(max_length=150, blank=True)
    desired_salary = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def __str__(self):
        return self.full_name


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    company_size = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.created_at:%Y-%m-%d}"
