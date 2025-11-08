from django.contrib import admin
from .models import Service, Project, TeamMember, Testimonial, ProjectRequest, SiteSetting, Job, JobApplication


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'order', 'created_at']
    list_editable = ['featured', 'order']
    list_filter = ['category', 'featured', 'created_at']
    search_fields = ['title', 'description', 'client_name']
    filter_horizontal = []


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'designation']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company_name', 'rating', 'featured', 'order', 'created_at']
    list_editable = ['featured', 'order', 'rating']
    list_filter = ['featured', 'rating', 'created_at']
    search_fields = ['client_name', 'company_name', 'testimonial_text']


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project_type', 'status', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['name', 'email', 'company_name', 'project_type']
    readonly_fields = ['submitted_at']
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company_name')
        }),
        ('Project Details', {
            'fields': ('project_type', 'budget', 'description')
        }),
        ('Administration', {
            'fields': ('status', 'notes', 'submitted_at')
        }),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Branding', {
            'fields': ('company_name', 'logo', 'tagline', 'website_url'),
            'description': 'Set your company name, upload logo, and add your website URL. Logo will appear in the header. Recommended logo size: 200x60px or similar aspect ratio.'
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address'),
            'description': 'Your contact details displayed on the website and footer.'
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'github_url'),
            'description': 'Add your social media profiles (optional).'
        }),
        ('Email Notification Settings', {
            'fields': ('notification_email', 'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'use_tls'),
            'description': 'Configure email settings to receive project requests via email. For Gmail, use smtp.gmail.com with port 587 and enable "Less secure app access" or use an App Password. For other providers, check their SMTP settings.'
        }),
    )
    
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'job_type', 'location', 'experience_level', 'is_active', 'featured', 'order', 'created_at']
    list_editable = ['is_active', 'featured', 'order']
    list_filter = ['job_type', 'experience_level', 'is_active', 'featured', 'department', 'created_at']
    search_fields = ['title', 'department', 'location', 'short_description', 'full_description', 'technologies']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'job_type', 'experience_level', 'location', 'salary_range')
        }),
        ('Job Description', {
            'fields': ('short_description', 'full_description')
        }),
        ('Requirements & Specifications', {
            'fields': ('requirements', 'responsibilities', 'preferred_qualifications', 'technologies')
        }),
        ('Additional Details', {
            'fields': ('benefits', 'application_deadline')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'featured', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job', 'email', 'phone', 'current_position', 'status', 'submitted_at']
    list_editable = ['status']
    list_filter = ['status', 'job', 'submitted_at']
    search_fields = ['full_name', 'email', 'phone', 'current_company', 'current_position']
    readonly_fields = ['submitted_at', 'updated_at']
    fieldsets = (
        ('Job Information', {
            'fields': ('job',)
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'current_location')
        }),
        ('Professional Information', {
            'fields': ('current_position', 'current_company', 'years_of_experience', 'linkedin_url', 'portfolio_url')
        }),
        ('Application Materials', {
            'fields': ('resume', 'cover_letter')
        }),
        ('Additional Information', {
            'fields': ('availability', 'expected_salary', 'notice_period')
        }),
        ('Administration', {
            'fields': ('status', 'notes', 'submitted_at', 'updated_at')
        }),
    )
