from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('content/<slug:slug>/', views.content_detail, name='content_detail'),
    path('project-detail/<slug:slug>/', views.project_detail_html, name='project_detail_html'),
    path('contact/', views.contact, name='contact'),
    path('health/', views.health_check, name='health_check'),
]