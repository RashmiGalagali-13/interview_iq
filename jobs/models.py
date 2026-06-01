from django.db import models
from accounts.models import User, CompanyProfile, JobSeekerProfile


class Job(models.Model):
    JOB_TYPE = (('full_time','Full Time'),('part_time','Part Time'),('contract','Contract'),('internship','Internship'),('remote','Remote'))
    EXPERIENCE_LEVEL = (('entry','Entry Level'),('mid','Mid Level'),('senior','Senior Level'),('executive','Executive'))
    STATUS = (('active','Active'),('closed','Closed'),('draft','Draft'))

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    skills_required = models.TextField(help_text='Comma-separated skills')
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL, default='mid')
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_skills_list(self):
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]

    def match_score(self, seeker_profile):
        if not seeker_profile:
            return 0
        job_skills = set(s.lower() for s in self.get_skills_list())
        seeker_skills = set(s.lower() for s in seeker_profile.get_skills_list())
        if not job_skills:
            return 0
        matched = job_skills.intersection(seeker_skills)
        return int((len(matched) / len(job_skills)) * 100)

    def __str__(self):
        return f"{self.title} @ {self.company.company_name}"

    class Meta:
        ordering = ['-created_at']


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_notes = models.TextField(blank=True)
    match_score = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.full_name} → {self.job.title}"


class SavedJob(models.Model):
    seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seeker', 'job')
