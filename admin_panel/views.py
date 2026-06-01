from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from accounts.models import User, JobSeekerProfile, CompanyProfile
from jobs.models import Job, Application
from interviews.models import InterviewQuestion, PracticeSession


def admin_required(view_func):
    """Decorator: only admin users can access."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_user():
            messages.error(request, "You do not have permission to access the admin panel.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    from accounts.models import ContactMessage
    stats = {
        'total_users': User.objects.count(),
        'total_seekers': User.objects.filter(user_type='jobseeker').count(),
        'total_companies': User.objects.filter(user_type='company').count(),
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(status='active').count(),
        'total_applications': Application.objects.count(),
        'pending_apps': Application.objects.filter(status='pending').count(),
        'accepted_apps': Application.objects.filter(status='accepted').count(),
        'total_questions': InterviewQuestion.objects.count(),
        'total_practice': PracticeSession.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    recent_users = User.objects.order_by('-date_joined')[:8]
    recent_apps = Application.objects.select_related('job__company', 'applicant').order_by('-applied_at')[:8]
    top_companies = CompanyProfile.objects.annotate(job_count=Count('jobs')).order_by('-job_count')[:5]
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_apps': recent_apps,
        'top_companies': top_companies,
        'recent_messages': recent_messages,
    })


@admin_required
def admin_users(request):
    q = request.GET.get('q', '')
    user_type = request.GET.get('type', '')
    users = User.objects.all().order_by('-date_joined')
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
    if user_type:
        users = users.filter(user_type=user_type)
    return render(request, 'admin_panel/manage_users.html', {
        'users': users, 'q': q, 'user_type': user_type,
    })


@admin_required
def admin_toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.warning(request, "You cannot deactivate your own account.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User '{user.username}' has been {status}.")
    return redirect('admin_users')


@admin_required
def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user == request.user:
            messages.warning(request, "You cannot delete your own account.")
        else:
            username = user.username
            user.delete()
            messages.success(request, f"User '{username}' deleted.")
    return redirect('admin_users')


@admin_required
def admin_jobs(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    jobs = Job.objects.select_related('company').order_by('-created_at')
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(company__company_name__icontains=q))
    if status:
        jobs = jobs.filter(status=status)
    return render(request, 'admin_panel/manage_jobs.html', {
        'jobs': jobs, 'q': q, 'status': status,
        'STATUS_CHOICES': Job.STATUS,
    })


@admin_required
def admin_toggle_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.status = 'closed' if job.status == 'active' else 'active'
    job.save()
    messages.success(request, f"Job '{job.title}' status updated to {job.get_status_display()}.")
    return redirect('admin_jobs')


@admin_required
def admin_delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f"Job '{title}' deleted.")
    return redirect('admin_jobs')


@admin_required
def admin_applications(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    apps = Application.objects.select_related('job__company', 'applicant').order_by('-applied_at')
    if q:
        apps = apps.filter(
            Q(applicant__full_name__icontains=q) |
            Q(job__title__icontains=q) |
            Q(job__company__company_name__icontains=q)
        )
    if status:
        apps = apps.filter(status=status)
    return render(request, 'admin_panel/manage_applications.html', {
        'applications': apps, 'q': q, 'status': status,
        'STATUS_CHOICES': Application.STATUS_CHOICES,
    })


@admin_required
def admin_update_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = [s[0] for s in Application.STATUS_CHOICES]
        if new_status in valid:
            app.status = new_status
            app.company_notes = request.POST.get('notes', app.company_notes)
            app.save()
            messages.success(request, f"Application status updated to {app.get_status_display()}.")
    return redirect('admin_applications')


@admin_required
def admin_questions(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    company_id = request.GET.get('company', '')
    questions = InterviewQuestion.objects.select_related('company').order_by('-created_at')
    if q:
        questions = questions.filter(Q(question__icontains=q) | Q(role_tag__icontains=q))
    if category:
        questions = questions.filter(category=category)
    if company_id:
        questions = questions.filter(company_id=company_id)
    companies = CompanyProfile.objects.all()
    return render(request, 'admin_panel/manage_questions.html', {
        'questions': questions, 'q': q, 'category': category,
        'CATEGORIES': InterviewQuestion.CATEGORY,
        'companies': companies,
        'selected_company': company_id,
    })


@admin_required
def admin_add_question(request):
    companies = CompanyProfile.objects.all()
    if request.method == 'POST':
        InterviewQuestion.objects.create(
            category=request.POST.get('category'),
            difficulty=request.POST.get('difficulty', 'medium'),
            role_tag=request.POST.get('role_tag', ''),
            question=request.POST.get('question'),
            sample_answer=request.POST.get('sample_answer'),
            tips=request.POST.get('tips', ''),
            company_id=request.POST.get('company') or None,
        )
        messages.success(request, "Question added successfully.")
        return redirect('admin_questions')
    return render(request, 'admin_panel/question_form.html', {
        'companies': companies,
        'CATEGORIES': InterviewQuestion.CATEGORY,
        'DIFFICULTIES': InterviewQuestion.DIFFICULTY,
        'action': 'Add',
    })


@admin_required
def admin_edit_question(request, pk):
    question = get_object_or_404(InterviewQuestion, pk=pk)
    companies = CompanyProfile.objects.all()
    if request.method == 'POST':
        question.category = request.POST.get('category')
        question.difficulty = request.POST.get('difficulty', 'medium')
        question.role_tag = request.POST.get('role_tag', '')
        question.question = request.POST.get('question')
        question.sample_answer = request.POST.get('sample_answer')
        question.tips = request.POST.get('tips', '')
        company_id = request.POST.get('company')
        question.company_id = company_id if company_id else None
        question.save()
        messages.success(request, "Question updated.")
        return redirect('admin_questions')
    return render(request, 'admin_panel/question_form.html', {
        'question': question,
        'companies': companies,
        'CATEGORIES': InterviewQuestion.CATEGORY,
        'DIFFICULTIES': InterviewQuestion.DIFFICULTY,
        'action': 'Edit',
    })


@admin_required
def admin_delete_question(request, pk):
    question = get_object_or_404(InterviewQuestion, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question deleted.")
    return redirect('admin_questions')


@admin_required
def admin_messages(request):
    """View and manage all contact messages."""
    from accounts.models import ContactMessage
    q = request.GET.get('q', '')
    is_read = request.GET.get('is_read', '')
    messages_list = ContactMessage.objects.order_by('-created_at')
    if q:
        messages_list = messages_list.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(message__icontains=q))
    if is_read:
        messages_list = messages_list.filter(is_read=True if is_read == 'read' else False)
    return render(request, 'admin_panel/manage_messages.html', {
        'messages_list': messages_list, 'q': q, 'is_read': is_read,
    })


@admin_required
def admin_toggle_message(request, pk):
    """Mark a contact message as read/unread."""
    from accounts.models import ContactMessage
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    status = "read" if msg.is_read else "unread"
    messages.success(request, f"Message marked as {status}.")
    return redirect('admin_messages')


@admin_required
def admin_delete_message(request, pk):
    """Delete a contact message."""
    from accounts.models import ContactMessage
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, "Message deleted.")
    return redirect('admin_messages')


# Admin Job Posting Views
@admin_required
def admin_post_job(request):
    from jobs.forms import JobForm
    from jobs.models import Job
    companies = CompanyProfile.objects.all().order_by('company_name')
    if request.method == 'POST':
        form = JobForm(request.POST)
        company_id = request.POST.get('company')
        if form.is_valid() and company_id:
            company = get_object_or_404(CompanyProfile, pk=company_id)
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, f"Job '{job.title}' posted successfully for {company.company_name}!")
            return redirect('admin_jobs')
        else:
            messages.error(request, "Please select a company.")
    else:
        form = JobForm()
    return render(request, 'admin_panel/post_job.html', {
        'form': form,
        'companies': companies,
        'action': 'Post',
        'JOB_TYPES': Job.JOB_TYPE,
        'EXPERIENCE_LEVELS': Job.EXPERIENCE_LEVEL,
        'STATUS': Job.STATUS,
    })


@admin_required
def admin_edit_job(request, pk):
    from jobs.forms import JobForm
    from jobs.models import Job
    job = get_object_or_404(Job, pk=pk)
    companies = CompanyProfile.objects.all().order_by('company_name')
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        company_id = request.POST.get('company')
        if form.is_valid() and company_id:
            company = get_object_or_404(CompanyProfile, pk=company_id)
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, f"Job '{job.title}' updated successfully!")
            return redirect('admin_jobs')
        else:
            messages.error(request, "Please select a company.")
    else:
        form = JobForm(instance=job)
    return render(request, 'admin_panel/post_job.html', {
        'form': form,
        'companies': companies,
        'job': job,
        'action': 'Edit',
        'JOB_TYPES': Job.JOB_TYPE,
        'EXPERIENCE_LEVELS': Job.EXPERIENCE_LEVEL,
        'STATUS': Job.STATUS,
    })
