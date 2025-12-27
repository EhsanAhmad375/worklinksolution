from django.urls import path
from . import admin_views

urlpatterns = [
    # Authentication
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    
    # Dashboard
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Services
    path('services/', admin_views.admin_services, name='admin_services'),
    path('services/create/', admin_views.admin_service_create, name='admin_service_create'),
    path('services/edit/<int:id>/', admin_views.admin_service_edit, name='admin_service_edit'),
    path('services/delete/<int:id>/', admin_views.admin_service_delete, name='admin_service_delete'),
    
    # Projects
    path('projects/', admin_views.admin_projects, name='admin_projects'),
    path('projects/create/', admin_views.admin_project_create, name='admin_project_create'),
    path('projects/edit/<int:id>/', admin_views.admin_project_edit, name='admin_project_edit'),
    path('projects/delete/<int:id>/', admin_views.admin_project_delete, name='admin_project_delete'),
    
    # Team Members
    path('team/', admin_views.admin_team, name='admin_team'),
    path('team/create/', admin_views.admin_team_create, name='admin_team_create'),
    path('team/edit/<int:id>/', admin_views.admin_team_edit, name='admin_team_edit'),
    path('team/delete/<int:id>/', admin_views.admin_team_delete, name='admin_team_delete'),
    
    # Testimonials
    path('testimonials/', admin_views.admin_testimonials, name='admin_testimonials'),
    path('testimonials/create/', admin_views.admin_testimonial_create, name='admin_testimonial_create'),
    path('testimonials/edit/<int:id>/', admin_views.admin_testimonial_edit, name='admin_testimonial_edit'),
    path('testimonials/delete/<int:id>/', admin_views.admin_testimonial_delete, name='admin_testimonial_delete'),
    
    # Project Requests
    path('project-requests/', admin_views.admin_project_requests, name='admin_project_requests'),
    path('project-requests/<int:id>/', admin_views.admin_project_request_detail, name='admin_project_request_detail'),
    
    # Jobs
    path('jobs/', admin_views.admin_jobs, name='admin_jobs'),
    path('jobs/create/', admin_views.admin_job_create, name='admin_job_create'),
    path('jobs/edit/<int:id>/', admin_views.admin_job_edit, name='admin_job_edit'),
    path('jobs/delete/<int:id>/', admin_views.admin_job_delete, name='admin_job_delete'),
    
    # Job Applications
    path('job-applications/', admin_views.admin_job_applications, name='admin_job_applications'),
    path('job-applications/<int:id>/', admin_views.admin_job_application_detail, name='admin_job_application_detail'),
    
    # Settings
    path('settings/', admin_views.admin_settings, name='admin_settings'),
]

