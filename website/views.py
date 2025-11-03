from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Service, Project, TeamMember, Testimonial, ProjectRequest


def home(request):
    """Homepage view with all sections"""
    services = Service.objects.filter(is_active=True)
    featured_projects = Project.objects.filter(featured=True)[:6]
    all_projects = Project.objects.all()[:9]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    testimonials = Testimonial.objects.filter(featured=True)[:6]
    
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
    ProjectRequest.objects.create(
        name=name,
        email=email,
        phone=phone,
        company_name=company_name,
        project_type=project_type,
        budget=budget,
        description=description,
    )
    
    messages.success(request, 'Thank you! We have received your project request. We will contact you soon.')
    return redirect('home')
