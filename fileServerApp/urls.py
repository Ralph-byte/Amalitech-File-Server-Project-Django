from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('feed/', views.feed, name='feed'),
    path('search/', views.search, name='search'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('send_email/<int:file_id>/', views.send_email, name='send_email'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('contact/', views.contact, name='contact'),
    
]