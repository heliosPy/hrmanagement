from django.urls import path
from interviewer import views


app_name = 'interviewer'


urlpatterns=[
    path('', views.interviewer_home, name='home'),
    path('profile/',views.view_profile, name='profile'),
    path('login/',views.interviewer_login, name='login'),
    path('logout', views.logout_interv, name='logout'),
    path('tinterview/', views.today_interviews, name='today_list'),
    path('tinterview/interview/<int:id>/', views.interview, name='interview'),
]