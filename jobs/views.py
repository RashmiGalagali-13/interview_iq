from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application, SavedJob
from .forms import JobForm, ApplicationForm, ApplicationStatusForm
from accounts.models import JobSeekerProfile


def job_list(request):
    jobs = Job.objects.filter(status='active').select_related('company')
    search = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('type', '')
    experience = request.GET.get('experience', '')

    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(skills_required__icontains=search) | Q(description__icontains=search))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if experience:
        jobs = jobs.filter(experience_level=experience)

    seeker_profile = None
    if request.user.is_authenticated and request.user.is_jobseeker():
        seeker_profile = request.user.seeker_profile

    job_data = []
    for job in jobs:
        score = job.match_score(seeker_profile) if seeker_profile else 0
        job_data.append({'job': job, 'score': score})

    if seeker_profile:
        job_data.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'jobs/job_list.html', {
        'job_data': job_data,
        'search': search,
        'location': location,
        'job_type': job_type,
        'experience': experience,
        'JOB_TYPES': Job.JOB_TYPE,
        'EXPERIENCE_LEVELS': Job.EXPERIENCE_LEVEL,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    is_saved = False
    match_score = 0

    if request.user.is_authenticated and request.user.is_jobseeker():
        profile = request.user.seeker_profile
        already_applied = Application.objects.filter(job=job, applicant=profile).exists()
        is_saved = SavedJob.objects.filter(seeker=profile, job=job).exists()
        match_score = job.match_score(profile)

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'is_saved': is_saved,
        'match_score': match_score,
    })


@login_required
def apply_job(request, pk):
    if not request.user.is_jobseeker():
        messages.error(request, "Only job seekers can apply.")
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk, status='active')
    profile = request.user.seeker_profile

    if Application.objects.filter(job=job, applicant=profile).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = profile
            app.match_score = job.match_score(profile)
            if not app.resume and profile.resume:
                app.resume = profile.resume
            app.save()
            messages.success(request, f"Successfully applied to {job.title}!")
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    if not request.user.is_jobseeker():
        return redirect('company_dashboard')
    profile = request.user.seeker_profile
    apps = profile.applications.select_related('job__company').all()
    return render(request, 'jobs/my_applications.html', {'applications': apps})


@login_required
def save_job(request, pk):
    if not request.user.is_jobseeker():
        messages.error(request, "Only job seekers can save jobs.")
        return redirect('job_list')
    job = get_object_or_404(Job, pk=pk)
    profile = request.user.seeker_profile
    saved, created = SavedJob.objects.get_or_create(seeker=profile, job=job)
    if not created:
        saved.delete()
        messages.info(request, "Job removed from saved list.")
    else:
        messages.success(request, "Job saved!")
    return redirect(request.META.get('HTTP_REFERER', 'job_list'))


# Company views
@login_required
def post_job(request):
    if not request.user.is_company():
        messages.error(request, "Only companies can post jobs.")
        return redirect('job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company_profile
            job.save()
            messages.success(request, f"Job '{job.title}' posted successfully!")
            return redirect('company_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})


@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated!")
            return redirect('company_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/post_job.html', {'form': form, 'edit': True, 'job': job})


@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted.")
        return redirect('company_dashboard')
    return render(request, 'jobs/confirm_delete.html', {'job': job})


@login_required
def recent_applications(request):
    if not request.user.is_company():
        return redirect('job_list')

    recent_apps = (
        Application.objects.filter(job__company=request.user.company_profile)
        .select_related('applicant', 'job')
        .order_by('-applied_at')
    )

    # Keep it simple for now: show top N recent apps.
    recent_apps = recent_apps[:50]

    return render(request, 'jobs/recent_applications.html', {
        'recent_apps': recent_apps,
    })


@login_required
def view_applications(request, job_pk):
    if not request.user.is_company():
        return redirect('job_list')
    job = get_object_or_404(Job, pk=job_pk, company=request.user.company_profile)
    applications = job.applications.select_related('applicant').order_by('-match_score', '-applied_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    highlight_app_pk = request.GET.get('app_pk')

    return render(request, 'jobs/view_applications.html', {
        'job': job,
        'applications': applications,
        'status_filter': status_filter,
        'STATUS_CHOICES': Application.STATUS_CHOICES,
        'highlight_app_pk': highlight_app_pk,
    })



@login_required
def update_application_status(request, app_pk):
    if not request.user.is_company():
        return redirect('job_list')
    app = get_object_or_404(Application, pk=app_pk, job__company=request.user.company_profile)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, f"Application status updated to {app.get_status_display()}.")
            return redirect('view_applications', job_pk=app.job.pk)
    else:
        form = ApplicationStatusForm(instance=app)
    return render(request, 'jobs/update_status.html', {'form': form, 'application': app})
