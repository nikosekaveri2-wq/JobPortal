from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Job, Application
from .forms import RegisterForm
from .ai_matcher import extract_resume_text, calculate_match

import requests


# ==================== JOBS ====================

def get_adzuna_jobs(search='', location='India'):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": 10,
        "what": search or "python developer",
        "where": location
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('results', [])

    return []


def home(request):
    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()

    jobs = Job.objects.all()

    if search:
        jobs = jobs.filter(
            title__icontains=search
        ) | jobs.filter(
            company__icontains=search
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    return render(request, 'home.html', {
        'jobs': jobs.distinct(),
        'adzuna_jobs': get_adzuna_jobs(
            search,
            location or 'India'
        ),
        'search': search,
        'location': location
    })


def job_detail(request, id):
    job = get_object_or_404(Job, id=id)

    return render(request, 'job_detail.html', {
        'job': job
    })


# ==================== APPLICATION ====================

@login_required(login_url='/login/')
def apply_job(request, id):
    job = get_object_or_404(Job, id=id)

    if Application.objects.filter(
        job=job,
        user=request.user
    ).exists():

        return render(request, 'apply.html', {
            'job': job,
            'errors': [
                'You have already applied for this job.'
            ]
        })

    if request.method == "POST":

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        resume = request.FILES.get('resume')

        errors = []

        if not name:
            errors.append("Name is required.")

        if not email:
            errors.append("Email is required.")
        elif '@' not in email:
            errors.append("Enter a valid email address.")

        if not phone:
            errors.append("Phone number is required.")
        elif not phone.isdigit() or len(phone) != 10:
            errors.append(
                "Phone number must be exactly 10 digits."
            )

        if not resume:
            errors.append("Resume is required.")
        elif not resume.name.lower().endswith(
            ('.pdf', '.docx')
        ):
            errors.append(
                "Resume must be PDF or DOCX."
            )

        if errors:
            return render(request, 'apply.html', {
                'job': job,
                'errors': errors,
                'name': name,
                'email': email,
                'phone': phone
            })

        # ==================== AI MATCHING ====================

        resume_text = extract_resume_text(resume)

        match_percentage = calculate_match(
            resume_text,
            job.description
        )

        # ==================== SAVE APPLICATION ====================

        Application.objects.create(
            job=job,
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            resume=resume,
            match_percentage=match_percentage
        )

        return redirect(
            'application_success',
            id=job.id
        )

    return render(request, 'apply.html', {
        'job': job
    })


@login_required(login_url='/login/')
def application_success(request, id):
    job = get_object_or_404(Job, id=id)

    application = Application.objects.filter(
        job=job,
        user=request.user
    ).first()

    return render(request, 'application_success.html', {
        'job': job,
        'application': application
    })


# ==================== AUTHENTICATION ====================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })


def user_login(request):

    error = ''

    if request.method == "POST":

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            auth_login(request, user)
            return redirect('home')

        error = 'Invalid username or password.'

    return render(request, 'login.html', {
        'error': error
    })


def user_logout(request):

    logout(request)

    return redirect('home')


# ==================== OTHER PAGES ====================

def jobs(request):

    return render(request, 'jobs.html', {
        'jobs': Job.objects.all()
    })


def companies(request):

    # Local database companies
    local_companies = list(
        Job.objects.values_list(
            'company',
            flat=True
        ).distinct()
    )

    # Adzuna API companies
    adzuna_jobs = get_adzuna_jobs(
        search='python developer',
        location='India'
    )

    api_companies = []

    for job in adzuna_jobs:

        company = job.get(
            'company',
            {}
        ).get(
            'display_name'
        )

        if company:
            api_companies.append(company)

    # Combine both
    companies = list(
        dict.fromkeys(
            local_companies + api_companies
        )
    )

    return render(request, 'companies.html', {
        'companies': companies
    })


def about(request):

    return render(request, 'about.html')