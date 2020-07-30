#this is the applicant/users application urls 
from django.urls import path

from applicant import views

app_name = 'users'

urlpatterns = [
    path('',views.user_home, name='home'),
    path('login/',views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('details/<int:id>/',views.recuir_detail, name='detail'),
    path('application/<int:id>/', views.apply_application, name='apply'),
    path('list/',views.recuir_list, name='current'),
    path('appied/', views.applied_list, name='applied')

]