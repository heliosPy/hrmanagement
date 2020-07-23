#this is the applicant/users application urls 
from django.urls import path

from applicant import views

app_name = 'users'

urlpatterns = [
    # path('', views.userhome, name='home'),
    path('login/',views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('home/',views.user_home, name='home')
]