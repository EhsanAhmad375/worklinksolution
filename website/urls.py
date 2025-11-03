from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-request/', views.submit_project_request, name='submit_project_request'),
]

