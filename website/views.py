from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage, get_connection
from django.http import JsonResponse
from .models import Service, Project, TeamMember, Testimonial, ProjectRequest, SiteSetting, Job, JobApplication


def home(request):
    """Homepage view with all sections"""
    services = Service.objects.filter(is_active=True)
    featured_projects = Project.objects.filter(featured=True)[:6]
    all_projects = Project.objects.all()[:9]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    testimonials = Testimonial.objects.all()[:6]
    featured_jobs = Job.objects.filter(is_active=True, featured=True)[:6]
    
    context = {
        'services': services,
        'featured_projects': featured_projects,
        'all_projects': all_projects,
        'team_members': team_members,
        'testimonials': testimonials,
        'featured_jobs': featured_jobs,
    }
    return render(request, 'website/home.html', context)


def careers(request):
    """Careers page with all active jobs"""
    jobs = Job.objects.filter(is_active=True).order_by('-featured', '-order', '-created_at')
    
    # Get unique filters for sidebar
    departments = Job.objects.filter(is_active=True).values_list('department', flat=True).distinct().exclude(department='')
    job_types = Job.objects.filter(is_active=True).values_list('job_type', flat=True).distinct()
    experience_levels = Job.objects.filter(is_active=True).values_list('experience_level', flat=True).distinct()
    locations = Job.objects.filter(is_active=True).values_list('location', flat=True).distinct()
    
    # Filter handling
    department_filter = request.GET.get('department', '')
    job_type_filter = request.GET.get('job_type', '')
    experience_filter = request.GET.get('experience', '')
    location_filter = request.GET.get('location', '')
    search_query = request.GET.get('search', '')
    
    if department_filter:
        jobs = jobs.filter(department=department_filter)
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)
    if experience_filter:
        jobs = jobs.filter(experience_level=experience_filter)
    if location_filter:
        jobs = jobs.filter(location=location_filter)
    if search_query:
        from django.db.models import Q
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(technologies__icontains=search_query)
        )
    
    context = {
        'jobs': jobs,
        'departments': departments,
        'job_types': job_types,
        'experience_levels': experience_levels,
        'locations': locations,
        'current_filters': {
            'department': department_filter,
            'job_type': job_type_filter,
            'experience': experience_filter,
            'location': location_filter,
            'search': search_query,
        }
    }
    return render(request, 'website/careers.html', context)


@require_http_methods(["POST"])
def submit_project_request(request):
    """Handle project request form submission"""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    company_name = request.POST.get('company_name', '').strip()
    project_type = request.POST.get('project_type', '').strip()
    budget = request.POST.get('budget', '').strip()
    description = request.POST.get('description', '').strip()
    
    # Basic validation
    if not name or not email or not project_type or not description:
        messages.error(request, 'Please fill in all required fields.')
        return redirect('home')
    
    # Create project request
    project_request = ProjectRequest.objects.create(
        name=name,
        email=email,
        phone=phone,
        company_name=company_name,
        project_type=project_type,
        budget=budget,
        description=description,
    )
    
    # Send email notification if email settings are configured
    try:
        site_settings = SiteSetting.objects.first()
        if site_settings and site_settings.notification_email and site_settings.smtp_host and site_settings.smtp_username and site_settings.smtp_password:
            # Configure email backend dynamically
            email_connection = get_connection(
                host=site_settings.smtp_host,
                port=site_settings.smtp_port,
                username=site_settings.smtp_username,
                password=site_settings.smtp_password,
                use_tls=site_settings.use_tls,
            )
            
            # Prepare email content
            subject = f"New Project Request: {project_type}"
            message = f"""
New project request received from your website:

Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}
Company: {company_name if company_name else 'Not provided'}
Project Type: {project_type}
Budget: {budget if budget else 'Not specified'}

Project Description:
{description}

---
This request has been saved in your admin panel.
"""
            
            # Send email
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=site_settings.smtp_username,
                to=[site_settings.notification_email],
                connection=email_connection,
            )
            email_message.send()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Error sending email notification: {str(e)}")
    
    messages.success(request, 'Thank you! We have received your project request. We will contact you soon.')
    return redirect('home')


@require_http_methods(["POST"])
def submit_job_application(request, job_id):
    """Handle job application form submission"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Get form data
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    current_location = request.POST.get('current_location', '').strip()
    current_position = request.POST.get('current_position', '').strip()
    current_company = request.POST.get('current_company', '').strip()
    years_of_experience = request.POST.get('years_of_experience', '0').strip()
    linkedin_url = request.POST.get('linkedin_url', '').strip()
    portfolio_url = request.POST.get('portfolio_url', '').strip()
    cover_letter = request.POST.get('cover_letter', '').strip()
    availability = request.POST.get('availability', '').strip()
    expected_salary = request.POST.get('expected_salary', '').strip()
    notice_period = request.POST.get('notice_period', '').strip()
    resume = request.FILES.get('resume')
    
    # Basic validation
    if not full_name or not email or not phone or not resume:
        messages.error(request, 'Please fill in all required fields including resume.')
        return redirect('home')
    
    # Validate file type
    allowed_extensions = ['.pdf', '.doc', '.docx']
    file_extension = resume.name.lower().split('.')[-1] if '.' in resume.name else ''
    if f'.{file_extension}' not in allowed_extensions:
        messages.error(request, 'Resume must be a PDF, DOC, or DOCX file.')
        return redirect('home')
    
    # Validate file size (max 5MB)
    if resume.size > 5 * 1024 * 1024:
        messages.error(request, 'Resume file size must be less than 5MB.')
        return redirect('home')
    
    try:
        years_exp = int(years_of_experience) if years_of_experience else 0
    except ValueError:
        years_exp = 0
    
    # Create job application
    job_application = JobApplication.objects.create(
        job=job,
        full_name=full_name,
        email=email,
        phone=phone,
        current_location=current_location,
        current_position=current_position,
        current_company=current_company,
        years_of_experience=years_exp,
        linkedin_url=linkedin_url,
        portfolio_url=portfolio_url,
        resume=resume,
        cover_letter=cover_letter,
        availability=availability,
        expected_salary=expected_salary,
        notice_period=notice_period,
    )
    
    # Send email notification if email settings are configured
    try:
        site_settings = SiteSetting.objects.first()
        if site_settings and site_settings.notification_email and site_settings.smtp_host and site_settings.smtp_username and site_settings.smtp_password:
            # Configure email backend dynamically
            email_connection = get_connection(
                host=site_settings.smtp_host,
                port=site_settings.smtp_port,
                username=site_settings.smtp_username,
                password=site_settings.smtp_password,
                use_tls=site_settings.use_tls,
            )
            
            # Prepare email content
            subject = f"New Job Application: {job.title} - {full_name}"
            message = f"""
New job application received for: {job.title}

Applicant Information:
Name: {full_name}
Email: {email}
Phone: {phone}
Location: {current_location if current_location else 'Not provided'}

Current Position: {current_position if current_position else 'Not provided'}
Current Company: {current_company if current_company else 'Not provided'}
Years of Experience: {years_exp}
LinkedIn: {linkedin_url if linkedin_url else 'Not provided'}
Portfolio: {portfolio_url if portfolio_url else 'Not provided'}

Additional Information:
Availability: {availability if availability else 'Not specified'}
Expected Salary: {expected_salary if expected_salary else 'Not specified'}
Notice Period: {notice_period if notice_period else 'Not specified'}

Cover Letter:
{cover_letter if cover_letter else 'No cover letter provided'}

---
Resume has been uploaded and saved in admin panel.
Application ID: {job_application.id}
"""
            
            # Send email with resume attachment
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=site_settings.smtp_username,
                to=[site_settings.notification_email],
                connection=email_connection,
            )
            # Attach resume
            if job_application.resume:
                email_message.attach(job_application.resume.name, job_application.resume.read(), 'application/pdf')
            email_message.send()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Error sending email notification: {str(e)}")
    
    messages.success(request, f'Thank you {full_name}! Your application for {job.title} has been submitted successfully. We will review it and get back to you soon.')
    return redirect('home')


def get_job_details(request, job_id):
    """Get job details as JSON for modal"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    job_data = {
        'id': job.id,
        'title': job.title,
        'department': job.department,
        'job_type': job.get_job_type_display(),
        'experience_level': job.get_experience_level_display(),
        'location': job.location,
        'salary_range': job.salary_range,
        'short_description': job.short_description,
        'full_description': job.full_description,
        'requirements': job.requirements,
        'responsibilities': job.responsibilities,
        'preferred_qualifications': job.preferred_qualifications,
        'technologies': job.technologies,
        'benefits': job.benefits,
        'application_deadline': job.application_deadline.strftime('%B %d, %Y') if job.application_deadline else None,
    }
    
    return JsonResponse(job_data)
