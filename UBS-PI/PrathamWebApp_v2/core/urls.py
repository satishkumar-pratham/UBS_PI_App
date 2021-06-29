from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.userLogin, name = 'core-userLogin'),
    path('about/', views.about, name = 'core-about'),
    path('home/', views.home, name = 'core-home'),
    path('userLogout/', views.userLogout, name = 'core-userLogout'),
    path('viewGuidelines/', views.viewGuidelines, name = 'core-viewGuidelines'),
    path('viewQuestions/', views.viewQuestions, name = 'core-viewQuestions'),
    path('uploadVideo/', views.uploadVideo, name = 'core-uploadVideo'),
    path('viewResults/', views.viewResults, name = 'core-viewResults'),
    path('recordVideo/', views.recordVideo, name = 'core-recordVideo'),
    
]
