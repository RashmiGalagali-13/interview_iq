from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobSeekerRegistrationForm, CompanyRegistrationForm, AdminRegistrationForm, CustomLoginForm, JobSeekerProfileForm, CompanyProfileForm, ContactForm
from .models import User, JobSeekerProfile, CompanyProfile, ContactMessage


def register_seeker(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.user_type = 'jobseeker'
            user.save()
            JobSeekerProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name']
            )
            messages.success(request, "Registration successful! Please log in to continue.")
            return redirect('login')
    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'accounts/register_seeker.html', {'form': form})


def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.user_type = 'company'
            user.save()
            CompanyProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                industry=form.cleaned_data['industry']
            )
            messages.success(request, "Company registration successful! Please log in to continue.")
            return redirect('login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/register_company.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_admin_user():
                return redirect('admin_dashboard')
            if user.is_company():
                return redirect('company_dashboard')
            return redirect('seeker_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def seeker_dashboard(request):
    if not request.user.is_jobseeker():
        return redirect('company_dashboard')
    profile = request.user.seeker_profile
    from jobs.models import Application, Job
    applications = profile.applications.select_related('job__company').order_by('-applied_at')[:5]
    saved = profile.saved_jobs.select_related('job__company').order_by('-saved_at')[:5]
    # Recommended jobs based on skills
    from jobs.models import Job as JobModel
    all_jobs = JobModel.objects.filter(status='active')
    recommended = sorted(all_jobs, key=lambda j: j.match_score(profile), reverse=True)[:6]
    return render(request, 'accounts/seeker_dashboard.html', {
        'profile': profile,
        'applications': applications,
        'saved_jobs': saved,
        'recommended': recommended,
    })


@login_required
def company_dashboard(request):
    if not request.user.is_company():
        return redirect('seeker_dashboard')
    profile = request.user.company_profile
    from jobs.models import Job, Application
    jobs = profile.jobs.all()
    recent_apps = Application.objects.filter(job__company=profile).order_by('-applied_at')[:10]
    stats = {
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(status='active').count(),
        'total_apps': Application.objects.filter(job__company=profile).count(),
        'pending_apps': Application.objects.filter(job__company=profile, status='pending').count(),
        'accepted_apps': Application.objects.filter(job__company=profile, status='accepted').count(),
    }
    return render(request, 'accounts/company_dashboard.html', {
        'profile': profile,
        'jobs': jobs,
        'recent_apps': recent_apps,
        'stats': stats,
    })


@login_required
def edit_seeker_profile(request):
    profile = request.user.seeker_profile
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('seeker_dashboard')
    else:
        form = JobSeekerProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile_type': 'seeker'})


@login_required
def company_website(request):
    if not request.user.is_company():
        return redirect('company_dashboard')
    return render(request, 'accounts/company_website.html')

@login_required
def edit_company_profile(request):
    profile = request.user.company_profile
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated!")
            return redirect('company_dashboard')
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile_type': 'company'})


def register_admin(request):
    # Allow anyone to register as admin (for demo purposes)
    # In production, you would restrict this to superusers only

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register_admin.html', {'form': AdminRegistrationForm()})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/register_admin.html', {'form': AdminRegistrationForm()})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'accounts/register_admin.html', {'form': AdminRegistrationForm()})
        
        # Create the admin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type='admin',
            is_staff=True,
            is_superuser=True
        )
        messages.success(request, "Admin account created successfully! Please log in.")
        return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'accounts/register_admin.html', {'form': form})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, "Your query has been submitted successfully! We will get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
