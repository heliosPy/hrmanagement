from django.urls import path
from hrhead import views

app_name= 'hrhead'

urlpatterns = [
    path('',views.hrhead_home, name='home'),
    path('profile/',views.view_profile, name='profile'),
    path('login/',views.hrhead_login, name='login'),
    path('logout', views.logout_hrhead, name='logout'),
    path('recuirtment/', views.recuirtmint_list, name='recuirtment'),
    path('result/<int:op>/', views.rescui_result, name='details' ),
]