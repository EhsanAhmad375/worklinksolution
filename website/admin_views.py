from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import (
    Service, Project, TeamMember, Testimonial, 
    ProjectRequest, SiteSetting, Job, JobApplication
)


def is_staff(user):
    """Check if user is staff"""
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    """Custom Admin Dashboard"""
    # Statistics
    stats = {
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(is_active=True).count(),
        'total_projects': Project.objects.count(),
        'featured_projects': Project.objects.filter(featured=True).count(),
        'total_team_members': TeamMember.objects.count(),
        'active_team_members': TeamMember.objects.filter(is_active=True).count(),
        'total_testimonials': Testimonial.objects.count(),
        'featured_testimonials': Testimonial.objects.filter(featured=True).count(),
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'total_job_applications': JobApplication.objects.count(),
        'pending_applications': JobApplication.objects.filter(status='pending').count(),
        'total_project_requests': ProjectRequest.objects.count(),
        'new_requests': ProjectRequest.objects.filter(status='new').count(),
    }
    
    # Recent Activity
    recent_projects = Project.objects.all().order_by('-created_at')[:5]
    recent_requests = ProjectRequest.objects.all().order_by('-submitted_at')[:5]
    recent_applications = JobApplication.objects.all().order_by('-submitted_at')[:5]
    
    context = {
        'stats': stats,
        'recent_projects': recent_projects,
        'recent_requests': recent_requests,
        'recent_applications': recent_applications,
    }
    return render(request, 'admin_panel/dashboard.html', context)


def admin_login(request):
    """Custom Admin Login"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password, or you do not have admin access.')
    
    return render(request, 'admin_panel/login.html')


@login_required
@user_passes_test(is_staff)
def admin_logout(request):
    """Custom Admin Logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


# ============================================
# SERVICES MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_services(request):
    """List all services"""
    services = Service.objects.all().order_by('order', 'title')
    context = {'services': services}
    return render(request, 'admin_panel/services/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_service_create(request):
    """Create new service"""
    if request.method == 'POST':
        service = Service.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            icon=request.POST.get('icon'),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, f'Service "{service.title}" created successfully!')
        return redirect('admin_services')
    return render(request, 'admin_panel/services/form.html', {'action': 'Create'})


@login_required
@user_passes_test(is_staff)
def admin_service_edit(request, id):
    """Edit service"""
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        service.title = request.POST.get('title')
        service.description = request.POST.get('description')
        service.icon = request.POST.get('icon')
        service.order = int(request.POST.get('order', 0))
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()
        messages.success(request, f'Service "{service.title}" updated successfully!')
        return redirect('admin_services')
    return render(request, 'admin_panel/services/form.html', {'service': service, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff)
def admin_service_delete(request, id):
    """Delete service"""
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        title = service.title
        service.delete()
        messages.success(request, f'Service "{title}" deleted successfully!')
        return redirect('admin_services')
    return render(request, 'admin_panel/services/delete.html', {'service': service})


# ============================================
# PROJECTS MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_projects(request):
    """List all projects"""
    projects = Project.objects.all().order_by('-created_at')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(client_name__icontains=search)
        )
    
    # Filter
    category = request.GET.get('category', '')
    if category:
        projects = projects.filter(category=category)
    
    featured = request.GET.get('featured', '')
    if featured == 'yes':
        projects = projects.filter(featured=True)
    elif featured == 'no':
        projects = projects.filter(featured=False)
    
    # Pagination
    paginator = Paginator(projects, 20)
    page = request.GET.get('page', 1)
    projects = paginator.get_page(page)
    
    context = {
        'projects': projects,
        'search': search,
        'category': category,
        'featured': featured,
    }
    return render(request, 'admin_panel/projects/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_project_create(request):
    """Create new project"""
    if request.method == 'POST':
        project = Project.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            technologies=request.POST.get('technologies', ''),
            client_name=request.POST.get('client_name', ''),
            project_url=request.POST.get('project_url', ''),
            featured=request.POST.get('featured') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        if 'image' in request.FILES:
            project.image = request.FILES['image']
            project.save()
        messages.success(request, f'Project "{project.title}" created successfully!')
        return redirect('admin_projects')
    return render(request, 'admin_panel/projects/form.html', {'action': 'Create'})


@login_required
@user_passes_test(is_staff)
def admin_project_edit(request, id):
    """Edit project"""
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.category = request.POST.get('category')
        project.technologies = request.POST.get('technologies', '')
        project.client_name = request.POST.get('client_name', '')
        project.project_url = request.POST.get('project_url', '')
        project.featured = request.POST.get('featured') == 'on'
        project.order = int(request.POST.get('order', 0))
        if 'image' in request.FILES:
            project.image = request.FILES['image']
        project.save()
        messages.success(request, f'Project "{project.title}" updated successfully!')
        return redirect('admin_projects')
    return render(request, 'admin_panel/projects/form.html', {'project': project, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff)
def admin_project_delete(request, id):
    """Delete project"""
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully!')
        return redirect('admin_projects')
    return render(request, 'admin_panel/projects/delete.html', {'project': project})


# ============================================
# TEAM MEMBERS MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_team(request):
    """List all team members"""
    team_members = TeamMember.objects.all().order_by('order', 'name')
    context = {'team_members': team_members}
    return render(request, 'admin_panel/team/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_team_create(request):
    """Create new team member"""
    if request.method == 'POST':
        member = TeamMember.objects.create(
            name=request.POST.get('name'),
            designation=request.POST.get('designation'),
            bio=request.POST.get('bio', ''),
            email=request.POST.get('email', ''),
            linkedin=request.POST.get('linkedin', ''),
            twitter=request.POST.get('twitter', ''),
            github=request.POST.get('github', ''),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on'
        )
        if 'photo' in request.FILES:
            member.photo = request.FILES['photo']
            member.save()
        messages.success(request, f'Team member "{member.name}" added successfully!')
        return redirect('admin_team')
    return render(request, 'admin_panel/team/form.html', {'action': 'Create'})


@login_required
@user_passes_test(is_staff)
def admin_team_edit(request, id):
    """Edit team member"""
    member = get_object_or_404(TeamMember, id=id)
    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.designation = request.POST.get('designation')
        member.bio = request.POST.get('bio', '')
        member.email = request.POST.get('email', '')
        member.linkedin = request.POST.get('linkedin', '')
        member.twitter = request.POST.get('twitter', '')
        member.github = request.POST.get('github', '')
        member.order = int(request.POST.get('order', 0))
        member.is_active = request.POST.get('is_active') == 'on'
        if 'photo' in request.FILES:
            member.photo = request.FILES['photo']
        member.save()
        messages.success(request, f'Team member "{member.name}" updated successfully!')
        return redirect('admin_team')
    return render(request, 'admin_panel/team/form.html', {'member': member, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff)
def admin_team_delete(request, id):
    """Delete team member"""
    member = get_object_or_404(TeamMember, id=id)
    if request.method == 'POST':
        name = member.name
        member.delete()
        messages.success(request, f'Team member "{name}" deleted successfully!')
        return redirect('admin_team')
    return render(request, 'admin_panel/team/delete.html', {'member': member})


# ============================================
# TESTIMONIALS MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_testimonials(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all().order_by('-created_at')
    context = {'testimonials': testimonials}
    return render(request, 'admin_panel/testimonials/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_testimonial_create(request):
    """Create new testimonial"""
    if request.method == 'POST':
        testimonial = Testimonial.objects.create(
            client_name=request.POST.get('client_name'),
            company_name=request.POST.get('company_name', ''),
            testimonial_text=request.POST.get('testimonial_text'),
            rating=int(request.POST.get('rating', 5)),
            featured=request.POST.get('featured') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        if 'client_photo' in request.FILES:
            testimonial.client_photo = request.FILES['client_photo']
            testimonial.save()
        messages.success(request, f'Testimonial from "{testimonial.client_name}" added successfully!')
        return redirect('admin_testimonials')
    return render(request, 'admin_panel/testimonials/form.html', {'action': 'Create'})


@login_required
@user_passes_test(is_staff)
def admin_testimonial_edit(request, id):
    """Edit testimonial"""
    testimonial = get_object_or_404(Testimonial, id=id)
    if request.method == 'POST':
        testimonial.client_name = request.POST.get('client_name')
        testimonial.company_name = request.POST.get('company_name', '')
        testimonial.testimonial_text = request.POST.get('testimonial_text')
        testimonial.rating = int(request.POST.get('rating', 5))
        testimonial.featured = request.POST.get('featured') == 'on'
        testimonial.order = int(request.POST.get('order', 0))
        if 'client_photo' in request.FILES:
            testimonial.client_photo = request.FILES['client_photo']
        testimonial.save()
        messages.success(request, f'Testimonial from "{testimonial.client_name}" updated successfully!')
        return redirect('admin_testimonials')
    return render(request, 'admin_panel/testimonials/form.html', {'testimonial': testimonial, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff)
def admin_testimonial_delete(request, id):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonial, id=id)
    if request.method == 'POST':
        name = testimonial.client_name
        testimonial.delete()
        messages.success(request, f'Testimonial from "{name}" deleted successfully!')
        return redirect('admin_testimonials')
    return render(request, 'admin_panel/testimonials/delete.html', {'testimonial': testimonial})


# ============================================
# PROJECT REQUESTS MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_project_requests(request):
    """List all project requests"""
    requests = ProjectRequest.objects.all().order_by('-submitted_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        requests = requests.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(project_type__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(requests, 20)
    page = request.GET.get('page', 1)
    requests = paginator.get_page(page)
    
    context = {
        'requests': requests,
        'status_filter': status_filter,
        'search': search,
    }
    return render(request, 'admin_panel/project_requests/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_project_request_detail(request, id):
    """View project request details"""
    req = get_object_or_404(ProjectRequest, id=id)
    if request.method == 'POST':
        req.status = request.POST.get('status')
        req.notes = request.POST.get('notes', '')
        req.save()
        messages.success(request, 'Project request updated successfully!')
        return redirect('admin_project_requests')
    return render(request, 'admin_panel/project_requests/detail.html', {'request': req})


# ============================================
# JOBS MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_jobs(request):
    """List all jobs"""
    jobs = Job.objects.all().order_by('-created_at')
    
    # Filter
    is_active = request.GET.get('is_active', '')
    if is_active == 'yes':
        jobs = jobs.filter(is_active=True)
    elif is_active == 'no':
        jobs = jobs.filter(is_active=False)
    
    featured = request.GET.get('featured', '')
    if featured == 'yes':
        jobs = jobs.filter(featured=True)
    elif featured == 'no':
        jobs = jobs.filter(featured=False)
    
    # Pagination
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page', 1)
    jobs = paginator.get_page(page)
    
    context = {
        'jobs': jobs,
        'is_active': is_active,
        'featured': featured,
    }
    return render(request, 'admin_panel/jobs/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_job_create(request):
    """Create new job"""
    if request.method == 'POST':
        job = Job.objects.create(
            title=request.POST.get('title'),
            department=request.POST.get('department', ''),
            job_type=request.POST.get('job_type'),
            experience_level=request.POST.get('experience_level'),
            location=request.POST.get('location'),
            salary_range=request.POST.get('salary_range', ''),
            short_description=request.POST.get('short_description'),
            full_description=request.POST.get('full_description'),
            requirements=request.POST.get('requirements'),
            responsibilities=request.POST.get('responsibilities'),
            preferred_qualifications=request.POST.get('preferred_qualifications', ''),
            technologies=request.POST.get('technologies', ''),
            benefits=request.POST.get('benefits', ''),
            application_deadline=request.POST.get('application_deadline') or None,
            is_active=request.POST.get('is_active') == 'on',
            featured=request.POST.get('featured') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, f'Job "{job.title}" created successfully!')
        return redirect('admin_jobs')
    return render(request, 'admin_panel/jobs/form.html', {'action': 'Create'})


@login_required
@user_passes_test(is_staff)
def admin_job_edit(request, id):
    """Edit job"""
    job = get_object_or_404(Job, id=id)
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.department = request.POST.get('department', '')
        job.job_type = request.POST.get('job_type')
        job.experience_level = request.POST.get('experience_level')
        job.location = request.POST.get('location')
        job.salary_range = request.POST.get('salary_range', '')
        job.short_description = request.POST.get('short_description')
        job.full_description = request.POST.get('full_description')
        job.requirements = request.POST.get('requirements')
        job.responsibilities = request.POST.get('responsibilities')
        job.preferred_qualifications = request.POST.get('preferred_qualifications', '')
        job.technologies = request.POST.get('technologies', '')
        job.benefits = request.POST.get('benefits', '')
        job.application_deadline = request.POST.get('application_deadline') or None
        job.is_active = request.POST.get('is_active') == 'on'
        job.featured = request.POST.get('featured') == 'on'
        job.order = int(request.POST.get('order', 0))
        job.save()
        messages.success(request, f'Job "{job.title}" updated successfully!')
        return redirect('admin_jobs')
    return render(request, 'admin_panel/jobs/form.html', {'job': job, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff)
def admin_job_delete(request, id):
    """Delete job"""
    job = get_object_or_404(Job, id=id)
    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f'Job "{title}" deleted successfully!')
        return redirect('admin_jobs')
    return render(request, 'admin_panel/jobs/delete.html', {'job': job})


# ============================================
# JOB APPLICATIONS MANAGEMENT
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_job_applications(request):
    """List all job applications"""
    applications = JobApplication.objects.all().order_by('-submitted_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Filter by job
    job_filter = request.GET.get('job', '')
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        applications = applications.filter(
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(applications, 20)
    page = request.GET.get('page', 1)
    applications = paginator.get_page(page)
    
    jobs = Job.objects.all()
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'job_filter': job_filter,
        'search': search,
        'jobs': jobs,
    }
    return render(request, 'admin_panel/job_applications/list.html', context)


@login_required
@user_passes_test(is_staff)
def admin_job_application_detail(request, id):
    """View job application details"""
    application = get_object_or_404(JobApplication, id=id)
    if request.method == 'POST':
        application.status = request.POST.get('status')
        application.notes = request.POST.get('notes', '')
        application.save()
        messages.success(request, 'Job application updated successfully!')
        return redirect('admin_job_applications')
    return render(request, 'admin_panel/job_applications/detail.html', {'application': application})


# ============================================
# SITE SETTINGS
# ============================================
@login_required
@user_passes_test(is_staff)
def admin_settings(request):
    """Site settings"""
    settings_obj, created = SiteSetting.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        settings_obj.company_name = request.POST.get('company_name')
        settings_obj.tagline = request.POST.get('tagline')
        settings_obj.website_url = request.POST.get('website_url', '')
        settings_obj.email = request.POST.get('email')
        settings_obj.phone = request.POST.get('phone')
        settings_obj.address = request.POST.get('address')
        settings_obj.facebook_url = request.POST.get('facebook_url', '')
        settings_obj.twitter_url = request.POST.get('twitter_url', '')
        settings_obj.linkedin_url = request.POST.get('linkedin_url', '')
        settings_obj.github_url = request.POST.get('github_url', '')
        settings_obj.notification_email = request.POST.get('notification_email', '')
        settings_obj.smtp_host = request.POST.get('smtp_host', '')
        settings_obj.smtp_port = int(request.POST.get('smtp_port', 587))
        settings_obj.smtp_username = request.POST.get('smtp_username', '')
        settings_obj.smtp_password = request.POST.get('smtp_password', '')
        settings_obj.use_tls = request.POST.get('use_tls') == 'on'
        
        if 'logo' in request.FILES:
            settings_obj.logo = request.FILES['logo']
        
        settings_obj.save()
        messages.success(request, 'Site settings updated successfully!')
        return redirect('admin_settings')
    
    return render(request, 'admin_panel/settings/form.html', {'settings': settings_obj})

