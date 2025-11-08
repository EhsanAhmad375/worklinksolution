from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('careers/', views.careers, name='careers'),
    path('submit-request/', views.submit_project_request, name='submit_project_request'),
    path('apply-job/<int:job_id>/', views.submit_job_application, name='submit_job_application'),
    path('job-details/<int:job_id>/', views.get_job_details, name='get_job_details'),
]

