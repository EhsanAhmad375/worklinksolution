from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Font Awesome icon class, e.g., 'fa-code'")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.title


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App'),
        ('desktop', 'Desktop Application'),
        ('ecommerce', 'E-Commerce'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies = models.CharField(max_length=300, help_text="Comma-separated, e.g., Django, React, PostgreSQL")
    client_name = models.CharField(max_length=200, blank=True)
    project_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-featured', '-order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    testimonial_text = models.TextField(validators=[MinLengthValidator(10)])
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-featured', '-order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.client_name} - {self.company_name}"


class ProjectRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    project_type = models.CharField(max_length=200, help_text="Type of project needed")
    budget = models.CharField(max_length=100, blank=True, help_text="Estimated budget range")
    description = models.TextField(help_text="Project requirements and details")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Project Request"
        verbose_name_plural = "Project Requests"
    
    def __str__(self):
        return f"{self.name} - {self.project_type}"


class SiteSetting(models.Model):
    company_name = models.CharField(max_length=200, default="TechSolutions Pro", help_text="Your company name (shown in header and footer)")
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload your company logo (recommended size: 200x60px)")
    tagline = models.CharField(max_length=300, default="Transforming Ideas into Digital Solutions", help_text="Company tagline or slogan")
    website_url = models.URLField(blank=True, null=True, help_text="Your company website URL")
    email = models.EmailField(default="info@techsolutionspro.com", help_text="Contact email address")
    phone = models.CharField(max_length=20, default="+1 (555) 123-4567", help_text="Contact phone number")
    address = models.TextField(default="123 Business Street, City, Country", help_text="Company address")
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn company page URL")
    github_url = models.URLField(blank=True, help_text="GitHub profile/company URL")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
