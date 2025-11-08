from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage, get_connection
from .models import Service, Project, TeamMember, Testimonial, ProjectRequest, SiteSetting


def home(request):
    """Homepage view with all sections"""
    services = Service.objects.filter(is_active=True)
    featured_projects = Project.objects.filter(featured=True)[:6]
    all_projects = Project.objects.all()[:9]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    testimonials = Testimonial.objects.all()[:6]
    
    context = {
        'services': services,
        'featured_projects': featured_projects,
        'all_projects': all_projects,
        'team_members': team_members,
        'testimonials': testimonials,
    }
    return render(request, 'website/home.html', context)


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
